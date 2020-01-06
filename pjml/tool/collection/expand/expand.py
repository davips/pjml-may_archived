from pjdata.collection import Collection
from pjml.tool.common.configless import ConfigLess


class Expand(ConfigLess):
    def _apply_impl(self, data):
        self.model = self.algorithm
        return Collection(data, data.history, data.failure, data.dataset)

    def _use_impl(self, data):
        return Collection(data, data.history, data.failure, data.dataset)
