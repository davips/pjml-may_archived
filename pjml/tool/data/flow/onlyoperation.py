# def onlyapply():
from pjml.tool.abc.nonconfigurablecontainer1 import NonConfigurableContainer1
from pjml.tool.abc.singleton import NoModel


class OnlyApply(NonConfigurableContainer1):
    """Does nothing during 'apply'."""

    # TODO: implement __new__ to generate a CS

    def _apply_impl(self, data):
        self.model = NoModel
        return self.transformer.apply(data)

    def _use_impl(self, data):
        return data


class OnlyUse(NonConfigurableContainer1):
    """Does nothing during 'apply'."""

    # TODO: implement __new__ to generate a CS

    def _apply_impl(self, data):
        self.model = NoModel
        return data

    def _use_impl(self, data):
        return self.transformer.use(data)
