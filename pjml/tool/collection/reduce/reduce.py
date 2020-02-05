from abc import ABC

from pjml.tool.base.mixin.functioninspector import FunctionInspector
from pjml.tool.base.transformer import Transformer


class Reduce(Transformer, FunctionInspector, ABC):
    def __init__(self, config, algorithm, deterministic=False):
        super().__init__(config, algorithm, deterministic)
        self.model = algorithm

    def _apply_impl(self, collection):
        return self._use_impl(collection)
