import hashlib
import json
from abc import ABC, abstractmethod
from functools import lru_cache

from pjdata.aux.encoders import dec
from pjdata.aux.identifyable import Identifyable
from pjdata.transformation import Transformation
from pjml.config.list import bag
from pjml.config.parameter import FixedP
from pjml.tool.base.aux.exceptionhandler import ExceptionHandler, \
    BadComponent, NoModel
from pjml.tool.base.aux.timers import Timers


class Transformer(Identifyable, dict, Timers, ExceptionHandler):
    """Parent of all processors, learners, evaluators, data controlers, ...

    Each component should decide by itself if it requires apply before use.
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
        # component without having to check if it is a class or an object.

        self.name = self.__class__.__name__
        self.path = self.__class__.__module__
        dict.__init__(self, transf=f'{self.name}@{self.path}', config=config)

    def __hash__(self):
        """Needed only because of lru_cache complaining about hashability of
        dict child classes."""
        if self._dump is None:
            self._dump = json.dumps(self, sort_keys=True)
        return int(hashlib.md5(self._dump.encode()).hexdigest(), 16)

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
            (probably meaning the pipeline finished before this component)
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
            (probably meaning the pipeline finished before this component)
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
        If called on an object, will convert the object to a config space
        with a single transformer.

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
        params = None if cs_.params is None else cs_.params.copy()
        name, path = cls.__name__, cls.__module__

        # Freeze args passed via kwargs # TODO: make real freeze inside the tree
        for k, v in kwargs.items():
            params[k] = FixedP(v)

        return cs_.updated(name=name, path=path, params=params)

    @property
    @lru_cache()
    def cs1(self=None):
        """Convert transformer into a config space with a single transformer
        inside it."""
        return bag(self)

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

    @classmethod
    def _get_class(cls, module, class_name):
        import importlib
        module = importlib.import_module(module)
        class_ = getattr(module, class_name)
        return class_

    def __str__(self, depth=''):
        rows = '\n'.join([f'  {k}: {v}' for k, v in self.config.items()])
        return f'{self.name} "{self.path}" [\n{rows}\n]'

    def _uuid_impl(self):
        return self.serialized

    @classmethod
    def _dict_to_transformer(cls, dic):
        """Convert recursively a dict to a transformer."""
        if 'transformer' not in dic:
            raise Exception('Provided dict does not represent a transformer.')
        name, path = dic['transformer'].split('@')
        cfg = dic['config']
        if 'component' in cfg:
            cfg['component'] = cls._dict_to_transformer(cfg['component'])

        return cls.materialize(name, path, cfg)

    @classmethod
    def materialize(cls, name, path, config):
        """Instantiate a transformer.

        Returns
        -------
        A ready to use component.
        """
        class_ = cls._get_class(path, name)
        return class_(**config)

    def clone(self):
        """Clone this transformer.

        Returns
        -------
        A ready to use component.
        """
        return self.materialize(self.name, self.path, self.config)

    @property
    @lru_cache()
    def serialized(self):
        if self._dump is None:
            self._dump = json.dumps(self, sort_keys=True)
        return self._dump

    @classmethod
    def deserialize(cls, txt):
        return cls._dict_to_transformer(json.loads(txt))

    @property
    @lru_cache()
    def transformer(self):
        """Helper function to avoid conditional Transformer vs Component.
        """
        return self
