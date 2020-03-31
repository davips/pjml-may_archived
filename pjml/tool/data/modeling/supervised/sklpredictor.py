from abc import ABC

from pjdata.step.use import Use

from pjml.tool.abc.mixin.enforceapply import EnforceApply
from pjml.tool.abc.mixin.exceptionhandler import BadComponent
from pjml.tool.data.sklalgorithm import SKLAlgorithm
from pjml.tool.model import Model


class SKLPredictor(SKLAlgorithm, EnforceApply, ABC):
    """
    Base class for classifiers, regressors, ... that implement fit/predict.
    """

    def _apply_impl(self, data_apply):
        sklearn_model = self.algorithm_factory()
        sklearn_model.fit(*data_apply.Xy)
        return Model(self, None, sklearn_model)

    def _use_impl(self, data_use, sklearn_model=None):
        return data_use.updated(
            self.transformations('a'),
            z=sklearn_model.predict(data_use.X)
        )

    def transformations(self, step):
        if step == 'a':
            return []
        elif step == 'u':
            return [Use(self, 0)]
        else:
            raise BadComponent('Wrong current step:', step)
