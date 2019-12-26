from pjdata.collection import Collection
from pjml.tool.base.transformer import Transformer


class NoAlgorithm:
    pass


class Expand(Transformer):
    def __init__(self):
        super().__init__({}, NoAlgorithm, isdeterministic=True)

    def _apply_impl(self, data):
        self.model = self.algorithm
        return Collection(data, data.history, data.failure, data.dataset)

    def _use_impl(self, data):
        return Collection(data, data.history, data.failure, data.dataset)

    @classmethod
    def _cs_impl(cls):
        raise Exception('It is not clear whether Expand should have a CS now.')
