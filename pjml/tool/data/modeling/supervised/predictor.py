from abc import ABC

from pjdata.step.use import Use
from pjml.tool.abc.mixin.enforceapply import EnforceApply
from pjml.tool.abc.mixin.exceptionhandler import BadComponent
from pjml.tool.model import Model
from pjml.tool.abc.transformer import Transformer


class Predictor(Transformer, EnforceApply, ABC):
    """
    Base class for classifiers, regressors, ... that implement fit/predict.
    """

    def __init__(self, config, algorithm_factory, sklearn_config=None,
                 deterministic=False):
        super().__init__(config, deterministic)
        self.algorithm_factory = algorithm_factory
        if sklearn_config is None:
            sklearn_config = config
        self.sklearn_config = sklearn_config

    def _apply_impl(self, data_apply):
        sklearn_model = self.algorithm_factory(**self.sklearn_config)
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
