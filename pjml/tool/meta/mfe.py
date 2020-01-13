from operator import itemgetter

from pjml.tool.base.singleton import NoAlgorithm
from pjml.config.cs.emptycs import EmptyCS
from pjml.tool.common.configless import ConfigLess
from pjml.tool.base.transformer import Transformer
from pymfe
import numpy as np


class MFE(Transformer):
    """Uniformly distribute examples along each attribute to make them
    independent of scale and unit measure.

    Each attribute value is replaced by the order in which the example is
    ranked according with that attribute.
    Applying a normalization after this transformer is recommended."""
    def __init__(self, **kwargs):
        super().__init__({}, NoAlgorithm, deterministic=True)
        self.mfe = pymfe.mfe.MFE()

    @classmethod
    def _cs_impl(cls):
        return EmptyCS()

    def _apply_impl(self, data):
        mfe.fit(*data.Xy)
        ft = mfe.extract()
        data.updated(self._transformation(), M=ft)

    def _use_impl(self, data):
        return self._apply_impl(data)
