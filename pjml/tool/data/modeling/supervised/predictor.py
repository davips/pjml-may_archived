from abc import ABC

from pjdata.step.use import Use
from pjml.tool.abc.mixin.exceptionhandler import BadComponent
from pjml.tool.abc.transformer import Transformer


class Predictor(Transformer, ABC):
    """
    Base class for classifiers, regressors, ... that implement fit/predict.
    """

    def _apply_impl(self, data):
        self.algorithm.fit(*data.Xy)
        self.model = self.algorithm
        return None

    def _use_impl(self, data):
        return data.updated(self._transformations(),
                            z=self.algorithm.predict(data.X))

    def _transformations(self, step=None, training_data=None):
        if step is None:
            step = self._current_step
        if training_data is None:
            training_data = self._last_training_data
        if step == 'a':
            return []
        elif step == 'u':
            return [Use(self, training_data)]
        else:
            raise BadComponent('Wrong current step:', step)
