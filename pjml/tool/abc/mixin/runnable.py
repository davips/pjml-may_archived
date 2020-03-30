from abc import ABC

from pjdata.data import Data
from pjml.tool.abc.mixin.exceptionhandler import ExceptionHandler
from pjml.tool.abc.mixin.timers import Timers


class RunnableApply(ExceptionHandler, Timers, ABC):
    # @abstractmethod
    # def transformations(self, step):
    #     pass

    def _run(self, function, data, exit_on_error=True, max_time=None):
        """Common procedure for apply() and use()."""
        from pjml.tool.model import Model
        from pjml.tool.abc.transformer import Transformer

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

            model = self._limit_by_time(function, data, max_time)

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


class RunnableUse(ExceptionHandler, Timers, ABC):
    # @abstractmethod
    # def transformations(self, step):
    #     pass

    def _run(self, function, data, exit_on_error=True, max_time=None):
        """Common procedure for apply() and use()."""
        from pjml.tool.model import Model
        from pjml.tool.abc.transformer import Transformer

        # Some data checking.
        if data and data.failure:
            return data
        self._check_nodata(data)

        # Detecting step.
        if data is None:
            return None
        if isinstance(data, Collection) and data.all_nones:
            return data
        if not isinstance(self, Model):
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

            output_data = self._limit_by_time(function, data, max_time)

            # Check result type.
            if not isinstance(output_data, (Data, Collection)):
                raise Exception(
                    f'{self.name()} does not handle {type(output_data)}!'
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

    def _no_use_impl(self, data, cause='failed'):
        raise Exception(
            f"A {self.name} model from {cause} pipelines during apply is not "
            f"usable!"
        )
