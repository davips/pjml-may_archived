from pjdata.data import Data
from pjdata.history import History
from pjdata.step.transformation import Transformation
from pjml.tool.abc.lighttransformer import LightTransformer
from pjml.tool.abc.mixin.nodatahandler import NoDataHandler

# Precisa herdar de Invisible, pois o mesmo Data pode vir de diferentes
# caminhos de arquivo (File) ou servidores (Source) e essas informações são
# irrelevantes para reprodutibilidade. Herdando de Invisible, o histórico é [].
from pjml.tool.model import Model


class New(LightTransformer, NoDataHandler):
    """Source of Data object from provided matrices."""

    def __init__(self, **kwargs):
        super().__init__(kwargs, deterministic=True)
        self.data = Data(History(self.transformations('u')), **kwargs)

    def _apply_impl(self, data):
        self._enforce_nodata(data, 'a')
        return Model(self, data, self.data)

    def _use_impl(self, data, **kwargs):
        self._enforce_nodata(data, 'u')
        return self.data

    @classmethod
    def _cs_impl(cls):
        raise Exception('I am not sure you should look for a CS here!')

    def transformations(self, step, clean=True):
        return [Transformation(self, 'u')]
