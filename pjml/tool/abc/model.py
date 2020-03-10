from pjdata.data import NoData, Data
from pjml.tool.abc.mixin.runnable import Runnable
from pjml.tool.abc.mixin.nodatahandler import NoDataHandler


class Model(Runnable, NoDataHandler):
    def __init__(self, data_from_apply, use_function, transformer):
        self._data_from_apply = data_from_apply
        self._use_function = use_function
        self._transformations_function = transformer.transformations
        self.name = transformer.name + ' Model'

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

        data_use: Data = self.data if own_data else data

        # TODO: Where should we set max_time?
        return self._run(self._use_function, data_use, exit_on_error)

    def transformations(self, step):
        return self._transformations_function(step)
