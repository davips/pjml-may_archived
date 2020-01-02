""" Scaler Module
"""
from abc import ABC

from pjml.tool.base.transformer import Transformer


class Scaler(Transformer, ABC):
    def _apply_impl(self, data):
        self.algorithm.fit(*data.Xy)
        self.model = self.algorithm
        return self._use_impl(data)

    def _use_impl(self, data):
        X = self.model.transform(data.X)
        return data.updated1(self._transformation(), X=X)
