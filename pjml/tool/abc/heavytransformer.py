from abc import abstractmethod, ABC
from functools import lru_cache

from pjdata.aux.decorator import classproperty
from pjdata.history import History
from pjdata.mixin.identifyable import Identifyable
from pjdata.aux.serialization import serialize, materialize
from pjdata.collection import Collection
from pjdata.data import Data
from pjdata.mixin.printable import Printable
from pjdata.step.transformation import Transformation

from pjml.config.description.cs.configlist import ConfigList
from pjml.tool.abc.mixin.exceptionhandler import BadComponent, ExceptionHandler
from pjml.tool.abc.mixin.timers import Timers
from pjml.tool.abc.transformer import Transformer
from pjml.tool.model import Model


class HeavyTransformer(Transformer, ABC):
    from pjdata.data import NoData

    def apply(self, data: Data = NoData, exit_on_error=True):
        collection_all_nones = isinstance(data, Collection) and data.all_nones
        if data is None or collection_all_nones:
            return Model(self, data, data,
                         use_impl=self._use_for_early_ended_pipeline)

        if data.failure:
            return Model(self, data, data,
                         use_impl=self._use_for_failed_pipeline)

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
            self._check_history(data, model.data, self.transformations('a'))

            # Check result type.
            if not isinstance(model, Model):
                raise Exception(f'{self.name} does not handle {type(model)}!')
        except Exception as e:
            self._handle_exception(e, exit_on_error)
            applied = data.updated(
                self.transformations('a'), failure=str(e)
            )
            model = Model(self, data, applied,
                          use_impl=self._use_for_failed_pipeline)
            # TODO: é possível que um container não complete o try acima?
            #  Caso sim, devemos gerar um ContainerModel aqui?

        # TODO: put time_spent inside data (as a "volatile" matrix)?
        time_spent = self._clock() - start
        self._dishandle_warnings()  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        return model

    def _use_for_early_ended_pipeline(self, data):
        raise Exception(
            f"A {self.name} model from early ended pipelines during apply is "
            f"not usable!"
        )

    def _use_for_failed_pipeline(self, data):
        raise Exception(
            f"A {self.name} model from failed pipelines during apply is not "
            f"usable!"
        )


