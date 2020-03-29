from abc import abstractmethod
from functools import lru_cache, partial

from pjdata.aux.decorator import classproperty
from pjdata.aux.identifyable import Identifyable
from pjdata.aux.serialization import serialize, materialize
from pjdata.data import NoData, Data
from pjdata.mixin.printable import Printable
from pjdata.step.apply import Apply
from pjdata.step.use import Use
from pjml.config.description.cs.configlist import ConfigList
from pjml.tool.abc.mixin.enforceapply import EnforceApply
from pjml.tool.abc.mixin.exceptionhandler import BadComponent
from pjml.tool.abc.mixin.runnable import Runnable
from pjml.tool.model import Model


class Transformer(Printable, Identifyable, Runnable):
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

    def __init__(self, config, deterministic=False):
        jsonable = {'id': f'{self.name}@{self.path}', 'config': config}
        Printable.__init__(self, jsonable)

        # TODO: we need to implement the random_state in the components
        if not deterministic and 'seed' in config:
            config['random_state'] = config.pop('seed')

        self.config = config
        self.deterministic = deterministic

        self._exit_on_error = True

        self.cs = self.cs1  # Shortcut to ease retrieving a CS from a
        # Transformer object without having to check that it is not a
        # component (Transformer class).

        self.max_time = None  # TODO: who/when to define maxtime?

    @abstractmethod
    def _apply_impl(self, data):
        """Each component should implement its core 'apply' functionality."""

    @classmethod
    @abstractmethod
    def _cs_impl(cls):
        """Each component should implement its own 'cs'. The parent class
        takes care of 'name' and 'path' arguments of ConfigSpace"""

    def transformations(self, step):
        """Ongoing transformation described as a list of Transformation
        objects.

        Child classes should override this method to perform non-atomic or
        non-trivial transformations.
        A missing implementation will be detected during apply/use."""
        if step == 'a':
            return [Apply(self)]
        elif step == 'u':
            return [Use(self, 0)]
        else:
            raise BadComponent('Wrong current step:', step)

    def apply(self, data: Data = NoData, exit_on_error=True):
        """Training step (usually).

        Fit/remove-noise-from/evaluate/... Data.

        Implementers: If your component requires apply() before use(),
        it should extend mixin EnforceApply and _apply_impl() should
        return (None, use_impl()) when provided data is None.

        Parameters
        ----------
        data
            'None' means 'pipeline ended before this transformation'.
            'NoData' means 'pipeline alive, hoping to generate Data in
            the next transformer'.
        exit_on_error
            Exit imediatly instead of just marking a failure inside Data object.

        Returns
        -------
        Transformed data, normally.
        None, when data is a None
            (probably meaning the pipeline finished before this transformer).
        Same data, but annotated with a failure.

        Exception
        ---------
        BadComponent
            Data resulting history should be consistent with
            _transformations() implementation.
        """
        if isinstance(self, EnforceApply) and data is None:
            use_impl = partial(
                self._no_use_impl,
                cause='early ended'
            )
            return Model(
                None, use_impl, self
            )

        # TODO: Where should we set max_time?
        return self._run(self._apply_impl, data, exit_on_error)

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
        return ConfigList(self)

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
        return serialize(self)

    # TODO: This work is to Edesio and Davi in the Future
    #
    # def _check_history(self, datain, dataout):
    #     """Check consistency between resulting Data object and
    #     _transformations() implementation provided by the current
    #     component."""
    #     if isinstance(dataout, NoData):
    #         return dataout
    #     recent = dataout.history.transformations[datain.history.size:]
    #     transfs = self.transformations(training_data=self._last_training_data)
    #     # print()
    #     # for t in transfs:
    #     #     t.disable_pretty_printing()
    #     #     print(t.name, t)
    #     if History(recent).id != History(transfs).id:
    #         print('\nTransformed Data object recent
    #         history:::::::::::::::::\n'
    #               f'{recent}\n'
    #               f'Expected
    #               transformations::::::::::::::::::::::::::::::::\n'
    #               f'{transfs}\n'
    #               'Transformed Data object history does not '
    #               'match expected transformation list.\n'
    #               'Please override self._transformations() '
    #               f'method for {self.name} or extend a proper parent class '
    #               f'like \'Invisible\'.')
    #         raise BadComponent(f'Inconsistent Data object history!')
    #     return dataout

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
    @lru_cache()
    def wrapped(self):
        """Same as unwrap(), but with the external container Wrap."""
        return None

    @property
    @lru_cache()
    def unwrap(self):
        """Subpipeline inside the first Wrap().

        Hopefully there is only one Wrap in the pipeline.
        This method performs a depth-first search.

        Example:
        pipe = Pipeline(
            File(name='iris.arff'),
            Wrap(Std(), SVMC()),
            Metric(function='accuracy')
        )
        pipe.unwrap  # -> Chain(Std(), SVMC())
        """
        return self.wrapped.transformer
