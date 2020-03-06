from pjdata.infinitecollection import InfiniteCollection
from pjml.tool.abc.configless import ConfigLess
from pjml.tool.abc.invisible import Invisible


class Expand(ConfigLess, Invisible):
    def _apply_impl(self, data):
        self.model = self.algorithm
        return InfiniteCollection(data, data.history, data.failure, data.dataset)

    def _use_impl(self, data):
        return InfiniteCollection(data, data.history, data.failure, data.dataset)
