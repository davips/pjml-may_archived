from abc import ABC

from pjdata.data import NoData
from pjml.tool.abc.transformer import Transformer


class NoDataHandler(Transformer, ABC):
    """All components that accept NoData should derive this class."""

    def _enforce_nodata(self, data):
        if data is not NoData:
            raise Exception(f'Component {self.name} needs to be applied with '
                            f'NoData. Use Sink before it if needed.')
