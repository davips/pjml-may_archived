from functools import lru_cache

from pjdata.data import NoData, Data
from pjml.tool.abc.mixin.exceptionhandler import ExceptionHandler
from pjml.tool.abc.mixin.timers import Timers


class Model(ExceptionHandler, Timers):
    _exit_on_error = True
    max_time = None  # TODO: who/when to define maxtime?

    def __init__(self, data_from_apply, use_function, transformations_function):
        self.data_from_apply = data_from_apply
        self.use_function = use_function
        self.transformations_function = transformations_function

    @property
    @lru_cache()
    def data(self):
        return self.data_from_apply

    def use(self, data=NoData, exit_on_error=True, own_data=False):
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

        # TODO: reduce replicated code between apply and use?
        data_use: Data = self.data if own_data else data
        if data_use is None:
            return None
        if data_use.failure:
            return data_use

        self._check_nodata(data_use)

        self._handle_warnings()  # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        start = self._clock()
        try:
            # Passa _exit_on_error para self de forma que
            # implementadores de conteineres possam acessar o valor
            # em _use_impl e repassar aos contidos.
            self._exit_on_error = exit_on_error

            output_data_use = self._limit_by_time(
                self.use_function, data_use, self.max_time
            )
        except Exception as use_exc:
            self._handle_exception(use_exc, exit_on_error)
            output_data_use = data_use.updated(
                self.transformations_function('u'), failure=str(use_exc)
            )

        time_spent_using = self._clock() - start
        self._dishandle_warnings()  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        return output_data_use
