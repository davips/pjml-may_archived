from abc import ABC
from functools import lru_cache

from pjdata.mixin.identifyable import Identifyable

from pjdata.abc.abstractdata import AbstractData
from pjdata.collection import Collection
from pjdata.data import Data
from pjml.tool.abc.mixin.exceptionhandler import ExceptionHandler
from pjml.tool.abc.mixin.nodatahandler import NoDataHandler
from pjml.tool.abc.mixin.timers import Timers


class Model(Identifyable, NoDataHandler, ExceptionHandler, Timers, ABC):
    """A possibly interpretable ML model able to make predictions, or,
    more generally, a data transformation.

    data_before_apply can be a data object or directly its uuid
    """
    from pjdata.data import NoData

    def __init__(self, transformer, data_before_apply,
                 data_after_apply, *args, use_impl=None):
        self.transformer = transformer
        self._use_impl = self.transformer._use_impl if use_impl is None else \
            use_impl

        if data_before_apply is None:
            raise Exception('None data_before_apply, eh normal isso?')
            # self._uuid_data_before_apply = Identifyable.nothing

        if isinstance(data_before_apply, AbstractData):
            self._uuid_data_before_apply = data_before_apply.uuid
        else:
            self._uuid_data_before_apply = data_before_apply

        self._data_after_apply = data_after_apply
        self.args = args

    def _uuid_impl(self):
        return 'm', self._uuid_data_before_apply + self.transformer.uuid

    def updated(self, transformer,
                data_before_apply=None, data_after_apply=None,
                args=None, use_impl=None):
        return self._updated(transformer,
                             data_before_apply, data_after_apply,
                             args=args, use_impl=use_impl)

    def _updated(self, transformer,
                 data_before_apply=None, data_after_apply=None,
                 models=None,
                 args=None, use_impl=None):
        # Update values.
        if transformer is None:
            raise Exception('Transformer cannot be None!')
        if data_before_apply is None:
            data_before_apply = self._uuid_data_before_apply
        if data_after_apply is None:
            data_after_apply = self._data_after_apply
        if args is None:
            args = self.args
        if use_impl is None:
            use_impl = self._use_impl

        # Handle ContainerModel specifics.
        if isinstance(self, ContainerModel):
            if models is None:
                models = self.models
            return ContainerModel(
                transformer,
                data_before_apply, data_after_apply,
                models,
                *args, use_impl=use_impl
            )

        return Model(
            transformer,
            data_before_apply, data_after_apply,
            *args, use_impl=use_impl
        )

    @property
    @lru_cache()
    def name(self):
        return f'Model[{self.transformer.name}]'

    @property
    def data(self):
        return self._data_after_apply

    def use(self, data: Data = NoData, exit_on_error=True, own_data=False):
        """Testing step (usually).

        Predict/transform/do nothing/evaluate/... Data.

        Parameters
        ----------
        own_data
        data
        exit_on_error

        Returns
        -------
        transformed data, normally
        None, when data is None
            (probably meaning the pipeline finished before this
            transformer)
        same data, but annotated with a failure

        Exception
        ---------
        BadComponent
            Data object resulting history should be consistent with
            _transformations() implementation.
        """
        data = self.data if own_data else data

        # Some data checking.
        if data and data.failure:
            return data
        self._check_nodata(data)

        # Detecting step.
        if data is None:
            return None
        if isinstance(data, Collection) and data.all_nones:
            return data

        # Disable warnings, measure time and make the party happen.
        self._handle_warnings()  # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        start = self._clock()
        try:
            # Aqui, passa-se _exit_on_error para self de forma que
            # implementadores de conteineres possam acessar o valor
            # dentro de
            # _apply_impl e repassar aos contidos. TODO: Mesmo p/ max_time?

            used = self._limit_by_time(self._use_impl,
                                       data, self.transformer.max_time,
                                       *self.args)
            self._check_history(data, used, self.transformations('u'))

            # Check result type.
            isdata_or_collection = isinstance(used, AbstractData)
            if not isdata_or_collection and used is not NoData:
                raise Exception(
                    f'{self.name} does not handle {type(used)}!\n'
                    f'{used}'
                )
        except Exception as e:
            self._handle_exception(e, exit_on_error)
            used = data.updated(
                self.transformations('u'), failure=str(e)
            )

        # TODO: put time_spent inside data (as a "volatile" matrix)?
        time_spent = self._clock() - start
        self._dishandle_warnings()  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # TODO: check_history to guide implementers whenever they need to
        #  implement transformations()

        return used

    def transformations(self, step):
        return self.transformer.transformations(step)


class ContainerModel(Model):
    def __init__(self, transformer, data_before_apply,
                 data_after_apply, models, *args,
                 use_impl=None):
        args = (models,) + args
        super().__init__(transformer, data_before_apply,
                         data_after_apply, *args, use_impl=use_impl)

        # ChainModel(ChainModel(a,b,c)) should be equal to ChainModel(a,b,c)
        if len(models) == 1 and isinstance(models[0], ContainerModel):
            models = models[0].models

        self.models = models

    def updated(self, transformer,
                data_before_apply=None, data_after_apply=None,
                models=None,
                args=None, use_impl=None):
        return self._updated(transformer,
                             data_before_apply, data_after_apply,
                             models=models,
                             args=args, use_impl=use_impl)
