from pjdata.data import NoData
from pjml.tool.base.singleton import NoModel
from pjml.tool.common.configless import ConfigLess


class Sink(ConfigLess):
    """End of Data object."""

    def __init__(self):
        super().__init__()
        self.model = NoModel

    def _apply_impl(self, data):
        return NoData

    def _use_impl(self, data):
        return NoData
