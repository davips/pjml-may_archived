from abc import ABC

from pjml.tool.base.aux.functioninspector import FunctionInspector
from pjml.tool.base.transformer import Transformer


class Reduce(Transformer, FunctionInspector, ABC):
    def __init__(self, config, algorithm, isdeterministic=False):
        super().__init__(config, algorithm, isdeterministic)
        self.model = algorithm

    def _apply_impl(self, collection):
        return self._use_impl(collection)
