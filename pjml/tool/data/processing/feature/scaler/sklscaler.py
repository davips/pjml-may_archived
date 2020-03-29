""" Scaler Module
"""
from abc import ABC

from pjml.tool.abc.transformer import Transformer
from pjml.tool.data.sklalgorithm import SKLAlgorithm
from pjml.tool.model import Model


class SKLScaler(SKLAlgorithm, ABC):
    def _apply_impl(self, data_apply):
        sklearn_model = self.algorithm_factory()
        sklearn_model.fit(*data_apply.Xy)

        def use_impl(data_use, step='u'):
            X = sklearn_model.transform(data_use.X)
            return data_use.updated(self.transformations(step), X=X)

        applied = use_impl(data_apply, step='a')
        return Model(applied, use_impl, self)
