from pjml.tool.common.container1 import Container1

# def alwaysapply():

class AlwaysApply(Container1):
    """Always 'apply' regardless of current step."""
    def _apply_impl(self, data):
        return self.transformer.apply(data)

    def _use_impl(self, data):
        return self.transformer.apply(data)

# def alwaysuse():

class AlwaysUse(Container1):
    """Always 'use' regardless of current step."""
    def _apply_impl(self, data):
        return self.transformer.use(data)

    def _use_impl(self, data):
        return self.transformer.use(data)
