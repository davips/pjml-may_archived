from pjdata.infinitecollection import InfiniteCollection

from pjml.tool.abc.configless import LightConfigLess
from pjml.tool.abc.invisible import Invisible
from pjml.tool.model.model import Model


class Expand(LightConfigLess, Invisible):
    def _apply_impl(self, data):
        applied = self._use_impl(data)
        return Model(self, data, applied)

    def _use_impl(self, data, **kwargs):
        return InfiniteCollection(data, data.history, data.failure)
