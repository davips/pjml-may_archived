from abc import ABC


class NoDataHandler(ABC):
    """All components that accept NoData should derive this class after
    deriving Transformer or descendants."""

    def _enforce_nodata(self, data, step):
        from pjdata.specialdata import NoData
        if step == 'a':
            step = 'applied'
        elif step == 'u':
            step = 'used'
        else:
            raise Exception('Wrong step', step)
        if data is not NoData:
            raise Exception(f'Component {self.name} needs to be {step} with '
                            f'NoData. Use Sink before it if needed.')
