from abc import ABC

from pjml.tool.base.transformer import Transformer


class Predictor(Transformer, ABC):
    """
    Base class for classifiers, regressors, ... that implement fit/predict.
    """

    def _apply_impl(self, data):
        self.algorithm.fit(*data.Xy)
        self.model = self.algorithm
        return None

    def _use_impl(self, data):
        return data.updated(self.transformation(), z=self.algorithm.predict(data.X))



