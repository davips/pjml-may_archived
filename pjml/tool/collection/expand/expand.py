from pjdata.collection import Collection
from pjml.tool.abc.configless import ConfigLess
from pjml.tool.abc.invisible import Invisible


class Expand(ConfigLess, Invisible):
    def _apply_impl(self, data):
        self.model = self.algorithm
        return Collection(data, data.history, data.failure, data.dataset)

    def _use_impl(self, data):
        return Collection(data, data.history, data.failure, data.dataset)
