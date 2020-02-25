from abc import ABC

from pjdata.step.apply import Apply
from pjdata.step.use import Use
from pjml.tool.abc.mixin.exceptionhandler import BadComponent
from pjml.tool.abc.transformer import Transformer


class Resampler(Transformer, ABC):
    """Base class for resampling methods. Not to be confused with Sample."""

    def _apply_impl(self, data):
        # TODO: generalize this to resample all fields (xyzuvwpq...) or
        #  create a parameter to define which fields to process
        X, y = self.algorithm.fit_resample(*data.Xy)
        self.model = self.algorithm
        return data.updated(self.transformations(), X=X, y=y)

    def _use_impl(self, data):
        return data

    def transformations(self, step=None, training_data=None):
        if step is None:
            step = self._current_step
        if training_data is None:
            training_data = self._last_training_data
        if step == 'a':
            return [Apply(self)]
        elif step == 'u':
            return []
        else:
            raise BadComponent('Wrong current step:', step)