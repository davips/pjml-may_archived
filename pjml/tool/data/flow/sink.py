from pjml.tool.abc.configless import LightConfigLess
from pjml.tool.model import Model


class Sink(LightConfigLess):
    """End of Data object."""

    def __init__(self):
        super().__init__()

    def _apply_impl(self, data):
        from pjdata.specialdata import NoData
        return Model(self, data, NoData)

    def _use_impl(self, data, **kwargs):
        from pjdata.specialdata import NoData
        return NoData
