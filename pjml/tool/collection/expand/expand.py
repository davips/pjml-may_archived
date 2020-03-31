from pjdata.infinitecollection import InfiniteCollection

from pjml.tool.abc.configless import LightConfigLess
from pjml.tool.abc.invisible import Invisible
from pjml.tool.model import Model


class Expand(LightConfigLess, Invisible):
    def _apply_impl(self, data_apply):
        applied = self._use_impl(data_apply)
        return Model(self, applied)

    def _use_impl(self, data_use, **kwargs):
        return InfiniteCollection(
            data_use, data_use.history, data_use.failure, data_use.dataset
        )
