from abc import abstractmethod, ABC
from functools import lru_cache

from pjdata.aux.decorator import classproperty
from pjdata.aux.identifyable import Identifyable
from pjdata.aux.serialization import serialize, materialize
from pjdata.collection import Collection
from pjdata.data import NoData, Data
from pjdata.mixin.printable import Printable
from pjdata.step.apply import Apply
from pjdata.step.use import Use

from pjml.config.description.cs.configlist import ConfigList
from pjml.tool.abc.mixin.exceptionhandler import BadComponent, ExceptionHandler
from pjml.tool.abc.mixin.timers import Timers
from pjml.tool.model import Model


class Transformer(Printable, Identifyable, ExceptionHandler, Timers, ABC):
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

    def __init__(self, config, deterministic=False, max_time=3600):
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

        self.max_time = max_time  # TODO: who/when to define maxtime?

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
        collection_all_nones = isinstance(data, Collection) and data.all_nones
        if data is None or collection_all_nones:
            return Model(data, self, self._use_for_early_ended_pipeline)

        if data.failure:
            return Model(data, self, self._use_for_failed_pipeline)

        self._check_nodata(data)

        # Disable warnings, measure time and make the party happen.
        self._handle_warnings()  # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        start = self._clock()
        try:
            # Aqui, passa-se _exit_on_error para self de forma que
            # implementadores de conteineres possam acessar o valor
            # dentro de
            # _apply_impl e repassar aos contidos. TODO: Mesmo p/ max_time?
            self._exit_on_error = exit_on_error

            model = self._limit_by_time(self._apply_impl, data, self.max_time)

            # Check result type.
            if not isinstance(model, Model):
                raise Exception(f'{self.name} does not handle {type(model)}!')
        except Exception as e:
            self._handle_exception(e, exit_on_error)
            output_data = data.updated(
                self.transformations('a'), failure=str(e)
            )
            model = Model(output_data, self, self._no_use_impl)
            # TODO: é possível que um container não complete o try acima?
            #  Caso sim, devemos gerar um ContainerModel aqui?

        # TODO: put time_spent inside data (as a "volatile" matrix)?
        time_spent = self._clock() - start
        self._dishandle_warnings()  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # TODO: usar check_history aqui, to guide implementers whenever they
        #  need to implement transformations()
        return model

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

    def _use_for_early_ended_pipeline(self, data, cause='failed'):
        raise Exception(
            f"A {self.name} model from early ended pipelines during apply is not "
            f"usable!"
        )

    def _use_for_failed_pipeline(self, data):
        raise Exception(
            f"A {self.name} model from failed pipelines during apply is not "
            f"usable!"
        )


class Transformer2(Transformer):
    @staticmethod
    @abstractmethod
    def _use_impl(self, data):
        """Each component should implement its core 'apply' functionality."""

    def apply(self, data: Data = NoData, exit_on_error=True):
        collection_all_nones = isinstance(data, Collection) and data.all_nones
        if data is None or collection_all_nones or data.failure:
            return Model(data, self, self._use_impl)

        self._check_nodata(data)

        # Disable warnings, measure time and make the party happen.
        self._handle_warnings()  # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        start = self._clock()
        try:
            # Aqui, passa-se _exit_on_error para self de forma que
            # implementadores de conteineres possam acessar o valor
            # dentro de
            # _apply_impl e repassar aos contidos. TODO: Mesmo p/ max_time?
            self._exit_on_error = exit_on_error

            model = self._limit_by_time(self._apply_impl, data, self.max_time)

            # Check result type.
            if not isinstance(model, Model):
                raise Exception(f'{self.name} does not handle {type(model)}!')
        except Exception as e:
            self._handle_exception(e, exit_on_error)
            output_data = data.updated(
                self.transformations('a'), failure=str(e)
            )
            model = Model(output_data, self, self._use_impl)
            # TODO: é possível que um container não complete o try acima?
            #  Caso sim, devemos gerar um ContainerModel aqui?

        # TODO: put time_spent inside data (as a "volatile" matrix)?
        time_spent = self._clock() - start
        self._dishandle_warnings()  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # TODO: usar check_history aqui, to guide implementers whenever they
        #  need to implement transformations()

        return model
