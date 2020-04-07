from pjml.tool.abc.configless import ConfigLess


class Sink(ConfigLess):
    """End of Data object."""
    from pjdata.data import NoData

    def __init__(self):
        super().__init__()

    def _apply_impl(self, data):
        return NoData

    def _use_impl(self, data):
        return NoData
