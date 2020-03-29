from abc import ABC

from pjdata.step.use import Use
from pjml.tool.abc.mixin.exceptionhandler import BadComponent
from pjml.tool.data.sklalgorithm import SKLAlgorithm
from pjml.tool.model import Model


class SKLPredictor(SKLAlgorithm, ABC):
    """
    Base class for classifiers, regressors, ... that implement fit/predict.
    """

    def _apply_impl(self, data_apply):
        sklearn_model = self.algorithm_factory()
        sklearn_model.fit(*data_apply.Xy)

        def use_impl(data_use):
            return data_use.updated(
                self.transformations('a'),
                z=sklearn_model.predict(data_use.X)
            )

        return Model(None, use_impl, self)

    def transformations(self, step=None):
        if step is None:
            step = self._current_step
        if step == 'a':
            return []
        elif step == 'u':
            return [Use(self, 0)]
        else:
            raise BadComponent('Wrong current step:', step)
