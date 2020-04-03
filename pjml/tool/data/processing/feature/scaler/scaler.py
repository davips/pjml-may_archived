""" Scaler Module
"""
from abc import ABC

from pjml.tool.abc.transformer import Transformer
from pjml.tool.data.algorithm import Algorithm
from pjml.tool.model import Model


class Scaler(Algorithm, ABC):
    def _apply_impl(self, data):
        sklearn_model = self.algorithm_factory()
        sklearn_model.fit(*data.Xy)

        applied = self._use_impl(data, sklearn_model, step='a')
        return Model(self, data, applied, sklearn_model)

    def _use_impl(self, data, sklearn_model=None, step='u'):
        X = sklearn_model.transform(data.X)
        return data.updated(self.transformations(step), X=X)
