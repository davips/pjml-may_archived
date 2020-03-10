from abc import ABC

from pjdata.data import Data
from pjml.tool.abc.mixin.exceptionhandler import ExceptionHandler
from pjml.tool.abc.mixin.timers import Timers


class Runnable(ExceptionHandler, Timers, ABC):
    # @abstractmethod
    # def transformations(self, step):
    #     pass

    def _run(self, function, data, exit_on_error=True, max_time=None):
        """Common procedure for apply() and use()."""
        from pjml.tool.abc.model import Model
        from pjml.tool.abc.transformer import Transformer

        # Some data checking.
        if data and data.failure:
            return data
        self._check_nodata(data)

        # Detecting step.
        if isinstance(self, Transformer):
            step = 'a'
        elif isinstance(self, Model):
            step = 'u'
            if data is None:
                return data
        else:
            raise Exception('Wrong implementation of runnable!', type(self))

        # Disable warnings, measure time and make the party happen.
        self._handle_warnings()  # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        start = self._clock()
        try:
            # Aqui, passa-se _exit_on_error para self de forma que
            # implementadores de conteineres possam acessar o valor
            # dentro de
            # _apply_impl e repassar aos contidos. TODO: Mesmo p/ max_time?
            self._exit_on_error = exit_on_error

            result = self._limit_by_time(
                function, data, max_time
            )

            # Check source of result: use, apply or apply-with-custom-model.
            if isinstance(result, Data):
                output_data, use_impl = result, None
            elif isinstance(result, tuple):
                output_data, use_impl = result
            elif isinstance(result, Model):
                raise Exception(
                    'Transformer cannot handle custom Model objects yet!'
                )
                # TODO: handle custom Model classes.
            else:
                raise Exception(
                    f'Unexpected return type: {type(result)}, value: '
                    f'{result}!'
                    f'\nStep: {step}'
                )
        except Exception as e:
            self._handle_exception(e, exit_on_error)
            output_data = data.updated(
                self.transformations(step), failure=str(e)
            )
            use_impl = self._no_use_impl

        # TODO: put time_spent inside data (as a "volatile" matrix)?
        time_spent = self._clock() - start
        self._dishandle_warnings()  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # TODO: check_history to guide implementers whenever they need to
        #  implement transformations()
        if use_impl is not None:
            return Model(output_data, use_impl, self)

        return output_data

    def _no_use_impl(self, data, cause='failed'):
        raise Exception(
            f"A {self.name} model from {cause} pipelines during apply is not "
            f"usable!"
        )
