from abc import ABC, abstractmethod
from functools import partial

from pjml.tool.abc.mixin.functioninspector import FunctionInspector
from pjml.tool.abc.transformer import Transformer
from pjml.tool.model import Model


class Reduce(Transformer, FunctionInspector, ABC):
    def __init__(self, config, deterministic=False):
        super().__init__(config, deterministic)
        self.function = self.function_from_name[config['function']]

    @staticmethod
    @abstractmethod
    def _use_impl(collection, function, transformations):
        pass

    def _apply_impl(self, collection):
        applied = self._use_impl(
            collection, self.function, self.transformations('a')
        )
        use_impl = partial(
            self._use_impl,
            function=self.function, transformations=self.transformations('u')
        )
        return Model(applied, self, use_impl)
