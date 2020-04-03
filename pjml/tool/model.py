from abc import ABC

from pjdata.aux.identifyable import Identifyable
from pjdata.collection import Collection
from pjdata.data import NoData, Data
from pjml.tool.abc.mixin.exceptionhandler import ExceptionHandler
from pjml.tool.abc.mixin.nodatahandler import NoDataHandler
from pjml.tool.abc.mixin.timers import Timers


class Model(Identifyable, NoDataHandler, ExceptionHandler, Timers, ABC):
    def __init__(self, transformer, data_before_apply,
                 data_after_apply, *args, use_impl=None):
        self.transformer = transformer
        self._use_impl = use_impl if use_impl else self.transformer._use_impl

        if data_before_apply:
            self._uuid_data_before_apply = data_before_apply.uuid
        else:
            self._uuid_data_before_apply = Identifyable.none

        self._data_after_apply = data_after_apply
        self._name = f'Model[{transformer.name}]'
        self.args = args

    def _uuid_impl(self):
        return 'm', self._uuid_data_before_apply + self.transformer.uuid

    def updated(self, responsible, transformer=None,
                data_before_apply=None, data_after_apply=None,
                args=None, use_impl=None):
        if transformer is None:
            transformer = self.transformer
        if data_after_apply is None:
            data_after_apply = self._data_after_apply
        if use_impl is None:
            use_impl = self._use_impl
        if args is None:
            args = self.args
        model = Model(transformer, data_before_apply,
                      data_after_apply, *args, use_impl=use_impl)
        model._name = f'Model[{responsible.name}[{model._name}]]'
        if data_before_apply is None:
            model._uuid_data_before_apply = self._uuid_data_before_apply
        return model

    def name(self):
        return self._name

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

            output_data = self._limit_by_time(self._use_impl,
                                              data, self.transformer.max_time,
                                              *self.args)

            # Check result type.
            if not isinstance(output_data, (Data, Collection, type)):
                raise Exception(
                    f'{self.name()} does not handle {type(output_data)}!\n'
                    f'{output_data}'
                )
        except Exception as e:
            self._handle_exception(e, exit_on_error)
            output_data = data.updated(
                self.transformations('u'), failure=str(e)
            )

        # TODO: put time_spent inside data (as a "volatile" matrix)?
        time_spent = self._clock() - start
        self._dishandle_warnings()  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # TODO: check_history to guide implementers whenever they need to
        #  implement transformations()

        return output_data

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

    def updated(self, responsible, transformer=None,
                data_before_apply=None, data_after_apply=None,
                models=None, args=None, use_impl=None):
        if transformer is None:
            transformer = self.transformer
        if data_after_apply is None:
            data_after_apply = self._data_after_apply
        if use_impl is None:
            use_impl = self._use_impl
        if args is None:
            args = self.args
        if models is None:
            models = self.models
        model = ContainerModel(
            transformer, data_before_apply,
            data_after_apply, models, *args, use_impl=use_impl
        )
        model._name = f'Model[{responsible.name}[{model._name}]]'
        if data_before_apply is None:
            model._uuid_data_before_apply = self._uuid_data_before_apply
        return model
