from abc import ABC


class NoDataHandler(ABC):
    """All components that accept NoData should derive this class after
    deriving Transformer or descendants."""

    def _enforce_nodata(self, data):
        from pjdata.data import NoData
        if data is not NoData:
            raise Exception(f'Component {self.name} needs to be applied with '
                            f'NoData. Use Sink before it if needed.')
