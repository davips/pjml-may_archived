from abc import ABC

from pjdata.step.apply import Apply
from pjml.tool.abc.mixin.exceptionhandler import BadComponent
from pjml.tool.data.sklalgorithm import SKLAlgorithm
from pjml.tool.model import Model


class SKLResampler(SKLAlgorithm, ABC):
    """Base class for resampling methods. Not to be confused with Sample."""

    def _apply_impl(self, data):
        # TODO: generalize this to resample all fields (xyzuvwpq...) or
        #  create a parameter to define which fields to process
        sklearn_model = self.algorithm_factory()
        X, y = sklearn_model.fit_resample(*data.Xy)
        applied = data.updated(self.transformations('a'), X=X, y=y)
        return Model(applied, self)

    def transformations(self, step):
        if step == 'a':
            return [Apply(self)]
        elif step == 'u':
            return []
        else:
            raise BadComponent('Wrong current step:', step)
