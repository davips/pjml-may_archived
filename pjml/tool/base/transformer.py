import json
from abc import abstractmethod
from functools import lru_cache

from pjdata.aux.identifyable import Identifyable
from pjdata.data import NoData

from pjdata.operation.apply import Apply
from pjdata.operation.use import Use
from pjml.config.cs.finitecs import FiniteCS
from pjml.config.cs.supercs import SuperCS
from pjml.tool.base.aux.decorator import classproperty
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
        self._current_operation = None
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

    def _transformation(self):
        """Ongoing transformation."""
        if self._current_operation == 'a':
            return Apply(self)
        else:
            return Use(self, self._last_training_data)

    def apply(self, data=NoData, exit_on_error=True):
        """Training step (usually).

        Fit/remove-noise-from/evaluate/... Data.

        Parameters
        ----------
        data
            'None' means 'pipeline ended before this transformation
            'NoData' means 'pipeline still alive, hoping to generate Data in
            one of the next transformers.
        exit_on_error

        Returns
        -------
        transformed data, normally
        None, when data is None
            (probably meaning the pipeline finished before this transformer)
        same data, but annotated with a failure
        """
        from pjml.tool.common.nodatatransformer import NoDataTransformer
        if data is NoData and not isinstance(self, NoDataTransformer):
            raise Exception(f'NoData is not accepted by {self.name}!')
        if data in [None, NoData]:
            # None = pipeline terminou antes desse transformer
            if self.model is None:
                # data=None and model=None:
                #   'apply' não consegue gerar modelo e o 'init' não o fez
                self.model = NoModel
                # model=NoModel:
                # não haverá modelo para o 'use', mas o pipeline deve continuar
        if data is None:
            return None

        if self.algorithm is None or self.config is None:
            raise BadComponent(f"{self} didn't set up "
                               f"an algorithm or a config at __init__. This"
                               f" should be done by calling the parent init")
        self._last_training_data = data
        self._current_operation = 'a'
        res = self._run(self._apply_impl, data, exit_on_error=exit_on_error)
        self._current_operation = None
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
        None, when data is None
            (probably meaning the pipeline finished before this transformer)
        same data, but annotated with a failure
        """
        from pjml.tool.common.nodatatransformer import NoDataTransformer
        if data is NoData and not isinstance(self, NoDataTransformer):
            raise Exception(f'NoData is not accepted by {self.name}!')
        # Sem data ou sem modelo (= pipeline interrompido no meio do 'apply'),
        # então "interrompe" também no 'use' (ou não, pois RF interrompe e
        # Cache deixa como nomodel qnd lê da base).
        if data is None:  # or self.model is NoModel:
            return None
        # if data is NoData:
        #     data = None

        if self._failure_during_apply is not None:
            return data.updated(
                failure=f'Already failed on apply: {self._failure_during_apply}')

        if self.model is None:
            raise MissingModel(f"{self}\n{self.name} didn't set up a model yet."
                               f" Method apply() should be called before use()!"
                               f"Another reason is a bad apply/init "
                               f"implementation.")

        self._current_operation = 'u'
        res = self._run(self._use_impl, data, exit_on_error=exit_on_error)
        self._current_operation = None
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
            output_data = data.updated(self._transformation(), failure=str(e))
        self.time_spent = self._clock() - start
        self._dishandle_warnings()  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        return output_data

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
        return json.dumps(self, sort_keys=False, indent=3)
