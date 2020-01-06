from abc import ABC

from pjml.tool.base.transformer import Transformer


class Resampler(Transformer, ABC):
    """Base class for resampling methods. Not to be confused with Sampler."""

    def _apply_impl(self, data):
        # TODO: generalize this to resample all fields (xyzuvwpq...) or
        #  create a parameter to define which fields to process
        X, y = self.algorithm.fit_resample(*data.Xy)
        self.model = self.algorithm
        return data.updated(self._transformation(), X=X, y=y)

    def _use_impl(self, data):
        return data
