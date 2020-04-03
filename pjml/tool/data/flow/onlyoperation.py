from pjdata.data import NoData, Data
from pjml.config.description.cs.containercs import ContainerCS
from pjml.tool.abc.nonconfigurablecontainer1 import NonConfigurableContainer1
from pjml.tool.abc.transformer import Transformer, LightTransformer
from pjml.tool.model import Model


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
        model = self.transformer.apply(data)
        return model.updated(self, use_impl=self._use_impl)

    def _use_impl(self, data, *args):
        return data

    def apply(self, data: Data = NoData, exit_on_error=True):
        # We are using the 'use()' method from LightTransformer
        # since OnlyApply transforms HeavyTransformer
        # in LightTransformer.
        return LightTransformer.apply(self, data, exit_on_error)


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
        return Model(self, data, data)

    def _use_impl(self, data, *args):
        return self.transformer._use_impl(data, *args)

    def apply(self, data: Data = NoData, exit_on_error=True):
        # We are using the 'use()' method from LightTransformer
        # since OnlyApply transforms HeavyTransformer
        # in LightTransformer.
        return LightTransformer.apply(self, data, exit_on_error)
