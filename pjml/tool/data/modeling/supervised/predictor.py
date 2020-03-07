from abc import ABC

from pjdata.step.use import Use
from pjml.tool.abc.mixin.exceptionhandler import BadComponent
from pjml.tool.abc.model import Model
from pjml.tool.abc.transformer import Transformer


class Predictor(Transformer, ABC):
    """
    Base class for classifiers, regressors, ... that implement fit/predict.
    """

    def __init__(self, config, algorithm_factory, sklearn_config,
                 deterministic=False):
        super().__init__(config, deterministic)
        self.algorithm_factory = algorithm_factory
        self.sklearn_config = sklearn_config

    def _apply_impl(self, data_apply):
        sklearn_model = self.algorithm_factory(**self.sklearn_config)
        sklearn_model.fit(*data_apply.Xy)

        class PredictorModel(Model):
            def _data_impl(self):
                return None

            def _use_impl(self, data_use):
                return data_use.updated(self.transformations(),
                                        z=sklearn_model.predict(data_use.X))

        return PredictorModel()

    def transformations(self, step=None, training_data=None):
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
