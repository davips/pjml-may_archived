import numpy as np
import pymfe.mfe

from pjml.config.description.cs.emptycs import EmptyCS
from pjml.tool.abc.singleton import NoAlgorithm
from pjml.tool.abc.transformer import Transformer


class MFE(Transformer):
    """Uniformly distribute examples along each attribute to make them
    independent of scale and unit measure.

    Each attribute value is replaced by the order in which the example is
    ranked according with that attribute.
    Applying a normalization after this transformer is recommended."""

    def __init__(self):
        super().__init__({}, NoAlgorithm, deterministic=True)
        self.model = pymfe.mfe.MFE()

    @classmethod
    def _cs_impl(cls):
        return EmptyCS()

    def _apply_impl(self, data):
        self.model.fit(*data.Xy)
        ft = self.model.extract()
        return data.updated(self._transformations(),
                            M=np.array([ft[1]]), Md=ft[0])

    def _use_impl(self, data):
        return self._apply_impl(data)
