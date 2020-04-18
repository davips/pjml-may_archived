from pjdata.aux.compression import pack_data
from pjdata.aux.encoders import UUID, prettydigest, md5digest
from pjdata.aux.serialization import serialize
from pjdata.data import Data
from pjdata.history import History

from pjdata.specialdata import NoData
from pjdata.step.transformation import Transformation
from pjml.tool.abc.lighttransformer import LightTransformer
from pjml.tool.abc.mixin.nodatahandler import NoDataHandler

# Precisa herdar de Invisible, pois o mesmo Data pode vir de diferentes
# caminhos de arquivo (File) ou servidores (Source) e essas informações são
# irrelevantes para reprodutibilidade. Herdando de Invisible, o histórico é [].
from pjml.tool.model.model import Model


class New(LightTransformer, NoDataHandler):
    """Source of Data object from provided matrices."""

    def __init__(self, **matrices):
        actual_hashes = {
            k: prettydigest(pack_data(v)) for k, v in matrices.items()
        }
        self._digest = md5digest(serialize(actual_hashes).encode())
        # TODO: will the matrices inside config break JSON, or cause other
        #  problems?
        super().__init__(matrices, deterministic=True)
        self.data = NoData.updated(self.transformations('u'), **matrices)
        # TODO: it is not clear whether this transformer is conceptually well
        #  behaved.

    def _apply_impl(self, data):
        self._enforce_nodata(data, 'a')
        return Model(self, data, self.data)

    def _use_impl(self, data, **kwargs):
        self._enforce_nodata(data, 'u')
        return self.data

    def _uuid_impl00(self):
        return UUID(self._digest)

    @classmethod
    def _cs_impl(cls):
        raise Exception('I am not sure you should look for a CS here!')

    def transformations(self, step, clean=True):
        return [Transformation(self, 'u')]
