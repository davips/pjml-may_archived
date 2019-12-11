from abc import ABC, abstractmethod
from functools import lru_cache

from pjdata.transformation import Transformation
from pjml.base.aux.exceptionhandler import ExceptionHandler, BadComponent, \
    NoModel
from pjml.base.aux.timers import Timers
from pjml.base.transformer import Transformer
from pjml.config.parameters import FixedP


class Component(ABC, Timers, ExceptionHandler):
    """Parent of all processors, learners, evaluators, data controlers, ...

    All components should implement:
        _apply_impl()
        _use_impl()
        _cs_impl()

    They also should, at __init__(), assign a value to:
        self.isdeterministic* (only when an override is needed)
        self.config¹
        self.algorithm²
    and at _apply_impl(), assign a value to:
        self.model³

    *: Deterministic components should override this class member with True.
    ¹: algorithm parameters
    ²: processor/learner/evaluator to apply()
    ³: induced/fitted/describing model to use()
    """

    # Mandatory fields.
    isdeterministic = False
    config = {}
    algorithm = None
    model = None

    _apply_failure = None
    last_operation = None

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

    @property
    @lru_cache()
    def transformer(self):
        """
        Returns
        -------
            A Transformer object able to recreate this component from scratch.
        """
        name, path = self.__class__.__name__, self.__module__
        return Transformer(name, path, self.config)

    def transformation(self):
        if self.last_operation is None:
            raise Exception(
                'transformation() should be called only after apply() or use()'
                ' operations!')
        return Transformation(self.transformer, self.last_operation)

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
            raise BadComponent(f"{self.transformer} didn't set up"
                               f"an algorithm or a config at __init__")
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
        if self._apply_failure is not None:
            return data.updated(failure=self._apply_failure)
        if self.model is None:
            raise NoModel(f"{self.transformer} didn't set up a model yet."
                          f" Method apply() should be called before use()!")
        self.last_operation = 'u'
        return self._run(self._use_impl, data)

    @classmethod
    def cs(cls, **kwargs):
        """Config Space of this component.

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
