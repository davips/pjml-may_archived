from abc import ABC

from pjml.base.aux.functioninspector import FunctionInspector
from pjml.base.component import Component


class Reduce(Component, FunctionInspector, ABC):
    def _apply_impl(self, collection):
        self.model = self.algorithm
        return self._use_impl(collection)
