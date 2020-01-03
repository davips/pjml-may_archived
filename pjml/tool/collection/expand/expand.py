from pjdata.collection import Collection
from pjml.tool.base.singleton import NoAlgorithm
from pjml.tool.common.noop import NoOp


class Expand(NoOp):
    def __init__(self):
        super().__init__({}, NoAlgorithm, deterministic=True)

    def _apply_impl(self, data):
        self.model = self.algorithm
        return Collection(data, data.history, data.failure, data.dataset)

    def _use_impl(self, data):
        return Collection(data, data.history, data.failure, data.dataset)
