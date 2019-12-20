from pjml.tool.base.component import Component


class ApplyUsing(Component):
    """Run a 'use' step right after an 'apply' one.

    Useful to calculate training error in classifiers, which would otherwise
    return None in the 'apply' step."""

    def __init__(self, component):
        super().__init__({'component': component}, component, True)
        self.model = self.algorithm

    def _apply_impl(self, data):
        self.model.apply(data)
        return self.model.use(data)

    def _use_impl(self, data):
        return self.model.use(data)

    @classmethod
    def _cs_impl(cls):
        pass
