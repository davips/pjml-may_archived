import hashlib
import json
from abc import abstractmethod
from functools import lru_cache

from pjdata.aux.identifyable import Identifyable
from pjdata.transformation import Transformation
from pjml.config.list import bag
from pjml.config.util import freeze
from pjml.tool.base.aux.decorator import classproperty
from pjml.tool.base.aux.exceptionhandler import ExceptionHandler, \
    BadComponent, NoModel
from pjml.tool.base.aux.serialization import materialize, serialize
from pjml.tool.base.aux.timers import Timers


class Transformer(Identifyable, dict, Timers, ExceptionHandler):
    """Parent of all processors, learners, evaluators, data controlers, ...

    Each component (alias for Transformer child class) implementation should
    decide by
    itself if it requires the 'apply' step before the 'use' step.
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
    _dump = None  # Needed because of conflicts between dict and lru_cache

    def __init__(self, config, algorithm, isdeterministic=False):
        if not isdeterministic and 'seed' in config:
            config['random_state'] = config.pop('seed')
        self.config = config
        self.algorithm = algorithm
        self.isdeterministic = isdeterministic

        self.model = None  # Mandatory field at apply() or init().
        self._failure_during_apply = None
        self.last_operation = None

        self.cs = self.cs1  # Shortcut to ease retrieving a CS from a
        # transformer (Transformer object) without having to check that it is
        # not a
        # component (Transformer class).

        dict.__init__(self, transf_id=f'{self.name}@{self.path}', config=config)

    @abstractmethod
    def _apply_impl(self, data):
        """Each component should implement its core 'apply' functionality."""

    @abstractmethod
    def _use_impl(self, data):
        """Each component should implement its core 'use' functionality."""

    # Class methods cannot be a property!
    # And should be classmethod, for this: KNN = KNN.cs()
    @classmethod
    @abstractmethod
    def _cs_impl(cls):
        """Each component should implement its own 'cs'. The parent class
        takes care of 'name' and 'path' arguments of ConfigSpace"""

    def transformation(self):
        if self.last_operation is None:
            raise Exception(
                'transformation() should be called only after apply() or use()'
                ' operations!')
        return Transformation(self, self.last_operation)

    def apply(self, data):
        """Training step (usually).

        Fit/remove-noise-from/evaluate/... Data.

        Parameters
        ----------
        data

        Returns
        -------
        transformed data, normally
        None, when data is None
            (probably meaning the pipeline finished before this transformer)
        same data, but annotated with a failure
        """
        if data is None:
            return None
        if self.algorithm is None or self.config is None:
            raise BadComponent(f"{self} didn't set up "
                               f"an algorithm or a config at __init__. This"
                               f" should be done by calling the parent init")
        self.last_operation = 'a'
        return self._run(self._apply_impl, data)

    def use(self, data):
        """Testing step (usually).

        Predict/transform/do nothing/evaluate/... Data.

        Parameters
        ----------
        data

        Returns
        -------
        transformed data, normally
        None, when data is None
            (probably meaning the pipeline finished before this transformer)
        same data, but annotated with a failure
        """
        if data is None:
            return None
        if self._failure_during_apply is not None:
            return data.updated(failure=self._failure_during_apply)
        if self.model is None:
            raise NoModel(f"{self} didn't set up a model yet."
                          f" Method apply() should be called before use()!"
                          f"Another reason is a bad apply/init implementation.")
        self.last_operation = 'u'
        return self._run(self._use_impl, data)

    @classmethod
    def cs(cls, **kwargs):
        """Config Space of this component, when called as class method.
        If called on an transformer (object/instance method), will convert
        the object to a config space with a single transformer.

        Each Config Space is a tree, where each path represents a parameter
        space of the learning/processing/evaluating algorithm of this component.
        It is a possibly infinite set of configurations.

        Parameters
        ----------
        kwargs
            If given, keyworded args are used to freeze some parameters of
            the algorithm, regardless of what a CS sampling could have chosen.
            TODO: it may be improved to effectively traverse and change the tree

        Returns
        -------
            Tree representing all the possible parameter spaces.
        """
        cs_ = cls._cs_impl()
        cs_ = freeze(cs_, **kwargs) if kwargs else cs_
        return cs_.updated(name=cls.__name__, path=cls.__module__)

    @property
    @lru_cache()
    def cs1(self=None):
        """Convert transformer into a config space with a single transformer
        inside it."""
        return bag(self)

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

    def _run(self, function, data, max_time=None):
        """Common procedure for apply() and use()."""
        if data.failure is not None:
            return data

        self._handle_warnings()  # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        start = self._clock()
        try:
            output_data = self._limit_by_time(function, data, max_time)
        except Exception as e:
            print('>>>>>>>>>>>>>>>>', e)
            self._handle_exception(e)
            output_data = data.updated(failure=str(e))
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

    def __hash__(self):  # Not memoizable due to infinite loop.
        """Needed only because of lru_cache complaining about hashability of
        dict child classes."""
        if self._dump is None:
            self._dump = json.dumps(self, sort_keys=True)
        return int(hashlib.md5(self._dump.encode()).hexdigest(), 16)

    def __str__(self, depth=''):
        rows = '\n'.join([f'  {k}: {v}' for k, v in self.config.items()])
        return f'{self.name} "{self.path}" [\n{rows}\n]'
