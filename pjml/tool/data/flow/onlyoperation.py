from pjml.tool.common.container1 import Container1

# def onlyapply():

class OnlyApply(Container1):
    """Does nothing during 'apply'."""
    def _apply_impl(self, data):
        return self.transformer.apply(data)

    def _use_impl(self, data):
        return data

# def onlyuse():

class OnlyUse(Container1):
    """Does nothing during 'apply'."""
    def _apply_impl(self, data):
        return data

    def _use_impl(self, data):
        return self.transformer.use(data)
