from pjml.config.description.cs.containercs import ContainerCS
from pjml.tool.abc.nonconfigurablecontainer1 import NonConfigurableContainer1
from pjml.tool.abc.singleton import NoModel
from pjml.tool.abc.transformer import Transformer


class OnlyApply(NonConfigurableContainer1):
    """Does nothing during 'apply'."""

    def __new__(cls, *args, transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            return object.__new__(cls)
        return ContainerCS(OnlyApply.name, OnlyApply.path, transformers)

    def _apply_impl(self, data):
        self.model = NoModel
        return self.transformer.apply(data)

    def _use_impl(self, data):
        return data


class OnlyUse(NonConfigurableContainer1):
    """Does nothing during 'apply'."""

    def __new__(cls, *args, transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            return object.__new__(cls)
        return ContainerCS(OnlyUse.name, OnlyUse.path, transformers)

    def _apply_impl(self, data):
        self.model = NoModel
        return data

    def _use_impl(self, data):
        return self.transformer.use(data)
