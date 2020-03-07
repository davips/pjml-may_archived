from abc import abstractmethod, ABC

from pjml.tool.abc.mixin.exceptionhandler import ExceptionHandler
from pjml.tool.abc.mixin.timers import Timers


class Runnable(ExceptionHandler, Timers, ABC):
    @abstractmethod
    def transformations(self):
        pass

    def _run(self, function, data, max_time=None, exit_on_error=True):
        """Common procedure for apply() and use()."""
        if data.failure:
            return data

        self._handle_warnings()  # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        start = self._clock()
        try:
            self._exit_on_error = exit_on_error
            output_model = self._limit_by_time(function, data, max_time)
        except Exception as e:
            self._handle_exception(e, exit_on_error)

            from pjml.tool.abc.model import Model

            class FailedModel(Model):
                def _data_impl(self):
                    return data.updated(self.transformations(), failure=str(e))

                def _use_impl(self, data):
                    raise Exception(
                        "A failed model doesn't have a Data object!"
                    )

            output_model = FailedModel()

        self.time_spent = self._clock() - start
        self._dishandle_warnings()  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        return output_model  # and self._check_history(data, output_data)
