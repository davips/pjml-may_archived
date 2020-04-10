from abc import ABC

from pjml.tool.abc.lighttransformer import LightTransformer
from pjml.tool.abc.mixin.functioninspector import FunctionInspector
from pjml.tool.model import Model


class Reduce(LightTransformer, FunctionInspector, ABC):
    def __init__(self, config, deterministic=False):
        super().__init__(config, deterministic)
        self.function = self.function_from_name[config['function']]

    def _apply_impl(self, collection):
        applied = self._use_impl(collection, step='a')
        return Model(self, collection, applied)
