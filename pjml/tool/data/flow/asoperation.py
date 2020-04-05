from pjml.tool.abc.minimalcontainer1 import MinimalContainer1


class AlwaysApply(MinimalContainer1):
    """Always 'apply' regardless of current step."""

    # TODO: implement __new__ to generate a CS

    def _apply_impl(self, data):
        self.model = NoModel
        return self.transformer.apply(data)

    def _use_impl(self, data):
        return self.transformer.apply(data)


class AlwaysUse(MinimalContainer1):
    """Always 'use' regardless of current step."""

    # TODO: implement __new__ to generate a CS

    def _apply_impl(self, data):
        self.model = NoModel
        return self.transformer.use(data)

    def _use_impl(self, data):
        return self.transformer.use(data)
