from pjdata.data import NoData, Data
from pjml.tool.abc.mixin.runnable import RunnableUse
from pjml.tool.abc.mixin.nodatahandler import NoDataHandler


class Model(RunnableUse, NoDataHandler):
    def __init__(self, data_from_apply, transformer, use_function=lambda x: x):
        self._data_from_apply = data_from_apply
        self._use_function = use_function
        self._transformations_function = transformer.transformations
        self._name = transformer.name + ' Model'

    def name(self):
        return self._name

    @property
    def data(self):
        return self._data_from_apply

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

        data_use = self.data if own_data else data

        # TODO: Where should we set max_time?
        return self._run(self._use_function, data_use, exit_on_error)

    def transformations(self, step):
        return self._transformations_function(step)


class ContainerModel(Model):
    def __init__(self, models, data_from_apply, transformer, use_function):
        super().__init__(data_from_apply, transformer, use_function)

        # ChainModel(ChainModel(a,b,c)) should be equal to ChainModel(a,b,c)
        if len(models) == 1 and isinstance(models[0], ContainerModel):
            models = models[0].models

        self.models = models
