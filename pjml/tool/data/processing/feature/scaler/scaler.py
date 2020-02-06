""" Scaler Module
"""
from abc import ABC

from pjml.tool.abc.transformer import Transformer


class Scaler(Transformer, ABC):
    def _apply_impl(self, data):
        self.algorithm.fit(*data.Xy)
        self.model = self.algorithm
        return self._use_impl(data)

    def _use_impl(self, data):
        X = self.model.transform(data.X)
        return data.updated(self._transformations(), X=X)
