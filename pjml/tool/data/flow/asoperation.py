from pjml.tool.common.nonconfigurablecontainer1 import NonConfigurableContainer1


class AlwaysApply(NonConfigurableContainer1):
    """Always 'apply' regardless of current step."""

    # TODO: implement __new__ to generate a CS

    def _apply_impl(self, data):
        return self.transformer.apply(data)

    def _use_impl(self, data):
        return self.transformer.apply(data)


class AlwaysUse(NonConfigurableContainer1):
    """Always 'use' regardless of current step."""

    # TODO: implement __new__ to generate a CS

    def _apply_impl(self, data):
        return self.transformer.use(data)

    def _use_impl(self, data):
        return self.transformer.use(data)
