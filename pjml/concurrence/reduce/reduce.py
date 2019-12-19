from abc import ABC

from pjml.base.aux.functioninspector import FunctionInspector
from pjml.base.component import Component


class Reduce(Component, FunctionInspector, ABC):
    def __init__(self, config, algorithm, isdeterministic=False):
        super().__init__(config, algorithm, isdeterministic)
        self.model = algorithm

    def _apply_impl(self, collection):
        return self._use_impl(collection)
