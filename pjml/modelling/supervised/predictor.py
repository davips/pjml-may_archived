from abc import ABC

from base.component import Component


class Predictor(Component, ABC):
    """
    Base class for classifiers, regressors, ... that implement fit/predict.
    """

    def _apply_impl(self, data):
        self.algorithm.fit(*data.Xy)
        self.model = self.algorithm
        return self._use_impl(data)

    def _use_impl(self, data):
        return data.updated(self, z=self.algorithm.predict(data.X))
