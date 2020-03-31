from abc import ABC

from pjdata.step.apply import Apply

from pjml.tool.abc.mixin.exceptionhandler import BadComponent
from pjml.tool.abc.transformer import Transformer2
from pjml.tool.model import Model


class SKLResampler(Transformer2, ABC):
    """Base class for resampling methods. Not to be confused with Sample."""
    def __init__(self, config, algorithm_factory, deterministic=False):
        super().__init__(config, deterministic)
        self.algorithm_factory = algorithm_factory

    def _apply_impl(self, data):
        # TODO: generalize this to resample all fields (xyzuvwpq...) or
        #  create a parameter to define which fields to process
        sklearn_model = self.algorithm_factory()
        X, y = sklearn_model.fit_resample(*data.Xy)
        applied = data.updated(self.transformations('a'), X=X, y=y)
        return Model(self, applied)

    def transformations(self, step):
        if step == 'a':
            return [Apply(self)]
        elif step == 'u':
            return []
        else:
            raise BadComponent('Wrong current step:', step)
