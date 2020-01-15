import json
from abc import abstractmethod
from functools import lru_cache

from pjdata.aux.identifyable import Identifyable
from pjdata.data import NoData, PhantomData
from pjdata.history import History

from pjdata.step.apply import Apply
from pjdata.step.use import Use
from pjml.config.cs.finitecs import FiniteCS
from pjml.config.cs.containercs import ContainerCS
from pjdata.aux.decorator import classproperty
from pjml.tool.base.aux.exceptionhandler import ExceptionHandler, \
    BadComponent, MissingModel
from pjml.tool.base.aux.serialization import materialize, serialize, \
    serialized_to_int
from pjml.tool.base.aux.timers import Timers
# from methodtools import lru_cache
from pjml.tool.base.singleton import NoModel


class Transformer(Identifyable, dict, Timers, ExceptionHandler):
    """Parent of all processors, learners, evaluators, data controlers, ...

    Contributors:

    Each component (alias for Transformer child classes) implementation should
    decide by itself if it requires the 'apply' step before the 'use' step.
    self.model should be set at the time of calling use().

    All components should implement:
        _apply_impl()
        _use_impl()
        _cs_impl()

    They also should call super.__init__(), assigning values to:
        config¹
        algorithm²
        isdeterministic*
    and at _apply_impl(), or before (at init), assign a value to:
        self.model³

    *: Deterministic components should override this class member with True.
    ¹: algorithm parameters
    ²: processor/learner/evaluator to apply()
    ³: induced/fitted/describing model to use()
    """
    _dump = None
    _hash = None  # Needed because of conflicts between dict and lru_cache,
    model = None  # Mandatory field at apply() or init().

    # cannot be in _init_ since _hash_ is called before _init_ is called.

    def __init__(self, config, algorithm, deterministic=False):
        if not deterministic and 'seed' in config:
            config['random_state'] = config.pop('seed')
        dict.__init__(self, id=f'{self.name}@{self.path}', config=config)

        self.config = config
        self.algorithm = algorithm
        self.deterministic = deterministic

        self._failure_during_apply = None
        self._current_step = None
        self._last_training_data = None
        self._exit_on_error = True

        self.cs = self.cs1  # Shortcut to ease retrieving a CS from a
        # Transformer object without having to check that it is not a
        # component (Transformer class).

    @abstractmethod
    def _apply_impl(self, data):
        """Each component should implement its core 'apply' functionality."""

    @abstractmethod
    def _use_impl(self, data):
        """Each component should implement its core 'use' functionality."""

    @classmethod
    @abstractmethod
    def _cs_impl(cls):
        """Each component should implement its own 'cs'. The parent class
        takes care of 'name' and 'path' arguments of ConfigSpace"""

    def _transformations(self, step=None, training_data=None):
        """Ongoing transformation described as a list of Transformation
        objects.

        Child classes should override the perform non-atomic or non-trivial
        transformations.
        A missing implementation will be detected during apply/use."""
        if step is None:
            step = self._current_step
        if training_data is None:
            training_data = self._last_training_data
        if step == 'a':
            return [Apply(self)]
        elif step == 'u':
            return [Use(self, training_data)]
        else:
            raise BadComponent('Wrong current step:', step)

    def apply(self, data=NoData, exit_on_error=True):
        """Training step (usually).

        Fit/remove-noise-from/evaluate/... Data.

        Parameters
        ----------
        data
            'PhantomData' means 'pipeline ended before this transformation
            'NoData' means 'pipeline still alive, hoping to generate Data in
            one of the next transformers.
        exit_on_error

        Returns
        -------
        transformed data, normally
        PhantomData, when data is a PhantomData object
            (probably meaning the pipeline finished before this transformer)
        same data, but annotated with a failure

        Exception
        ---------
        BadComponent
            Data object resulting history should be consistent with
            _transformations() implementation.
        """
        if data is NoData:
            from pjml.tool.common.transformer_nodata import Transformer_NoData
            if not isinstance(self, Transformer_NoData):
                raise Exception(f'NoData is not accepted by {self.name}!')
            if data.isphantom:
                # pipeline terminou antes desse transformer
                if self.model is None:
                    # 'apply' não vai conseguir gerar modelo pra um PhantomData
                    self.model = NoModel
        if data.isphantom:
            return data

        if self.algorithm is None or self.config is None:
            raise BadComponent(f"{self} didn't set up "
                               f"an algorithm or a config at __init__. This"
                               f" should be done by calling the parent init")
        self._last_training_data = data
        self._current_step = 'a'
        res = self._run(self._apply_impl, data, exit_on_error=exit_on_error)
        self._current_step = None
        return res

    def use(self, data=NoData, exit_on_error=True):
        """Testing step (usually).

        Predict/transform/do nothing/evaluate/... Data.

        Parameters
        ----------
        data
        exit_on_error

        Returns
        -------
        transformed data, normally
        PhantomData, when data is a PhantomData object
            (probably meaning the pipeline finished before this transformer)
        same data, but annotated with a failure

        Exception
        ---------
        BadComponent
            Data object resulting history should be consistent with
            _transformations() implementation.
        """
        from pjml.tool.common.transformer_nodata import Transformer_NoData
        if data is NoData and not isinstance(self, Transformer_NoData):
            raise Exception(f'NoData is not accepted by {self.name}!')
        # Sem data ou sem modelo (= pipeline interrompido no meio do 'apply'),
        # então "interrompe" também no 'use' (ou não, pois RF interrompe e
        # Cache deixa como nomodel qnd lê da base).
        if data.isphantom:
            return data

        if self._failure_during_apply is not None:
            return data.updated(
                failure=f'Already failed on apply: '
                        f'{self._failure_during_apply}')

        if self.model is None:
            raise MissingModel(f"{self}\n{self.name} didn't set up a model yet."
                               f" Method apply() should be called before use()!"
                               f"Another reason is a bad apply/init "
                               f"implementation.")

        self._current_step = 'u'
        res = self._run(self._use_impl, data, exit_on_error=exit_on_error)
        self._current_step = None
        return res

    # @classmethod  <-- Causes AttributeError:
    #           'functools._lru_cache_wrapper' object has no attribute 'sample'
    @classproperty
    @lru_cache()
    def cs(cls):
        """Config Space of this component, when called as class method.
        If called on an transformer (object/instance method), will convert
        the object to a config space with a single transformer.

        Each Config Space is a tree, where each path represents a parameter
        space of the learning/processing/evaluating algorithm of this component.
        It is a possibly infinite set of configurations.

        Returns
        -------
            Tree representing all the possible parameter spaces.
        """
        cs_ = cls._cs_impl()
        return cs_.identified(name=cls.__name__, path=cls.__module__)

    @property
    @lru_cache()
    def cs1(self=None):
        """Convert transformer into a config space with a single transformer
        inside it."""
        return FiniteCS(self)

    def clone(self):
        """Clone this transformer.

        Returns
        -------
        A ready to use transformer.
        """
        return materialize(self.name, self.path, self.config)

    @property
    @lru_cache()
    def serialized(self):
        if self._dump is None:
            self._dump = serialize(self)
        return self._dump

    def _run(self, function, data, max_time=None, exit_on_error=True):
        """Common procedure for apply() and use()."""
        if data.failure:
            return data

        self._handle_warnings()  # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        start = self._clock()
        try:
            self._exit_on_error = exit_on_error
            output_data = self._limit_by_time(function, data, max_time)
        except Exception as e:
            self._handle_exception(e, exit_on_error)
            output_data = data.updated(self._transformations(), failure=str(e))
        self.time_spent = self._clock() - start
        self._dishandle_warnings()  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        return output_data and self._check_history(data, output_data)

    def _check_history(self, datain, dataout):
        """Check consistency between resulting Data object and provided
        _transformations() implementation."""
        if isinstance(dataout, NoData):
            return dataout
        recent = dataout.history.transformations[datain.history.size:]
        print('_____________________________')
        for t in self._transformations():
            print(t.uuid, t.name, t)
        print(']]]]]]]]]]]]]]]]]]]]]]]]]')
        for t in recent:
            print(t.uuid, t.name, t)
        print('.........................')
        if History(recent).uuid != History(self._transformations()).uuid:
            print('\nTransformed Data object recent history:::::::::::::::::\n'
                  f'{recent}\n'
                  f'Expected transformations::::::::::::::::::::::::::::::::\n'
                  f'{self._transformations()}\n'
                  'Transformed Data object history does not '
                  'match expected transformation list.\n'
                  'Please override self._transformations() '
                  f'method for {self.name} or extend a proper parent class '
                  f'like \'Invisible\'.')
            raise BadComponent(f'Inconsistent Data object history!')
        return dataout

    @staticmethod
    def _to_config(locals_):
        """Convert a dict coming from locals() to config."""
        config = locals_.copy()
        del config['self']
        del config['__class__']
        return config

    def _uuid_impl(self):
        return self.serialized

    @classproperty
    @lru_cache()
    def name(cls):
        return cls.__name__

    @classproperty
    @lru_cache()
    def path(cls):
        return cls.__module__

    @property
    def wrapped(self):
        return None

    def __hash__(self):  # This method is not memoizable due to infinite loop.
        """Needed only because of lru_cache complaining about hashability of
        dict child classes."""
        if self._dump is None:
            self._dump = serialize(self)  # Cannot call self.serialized here!
        if self._hash is None:
            self._hash = serialized_to_int(self._dump)
        return self._hash

    def __str__(self, depth=''):
        return json.dumps(self, sort_keys=False)  # , indent=3)
