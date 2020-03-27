from abc import ABC, abstractmethod

from pjdata.data import NoData


class NoDataHandler(ABC):
    """All components that accept NoData should derive this class after
    deriving Transformer or descendants."""

    @classmethod
    @abstractmethod
    def name(cls):
        pass

    def _enforce_nodata(self, data):
        if data is not NoData:
            raise Exception(f'Component {self.name} needs to be applied with '
                            f'NoData. Use Sink before it if needed.')
