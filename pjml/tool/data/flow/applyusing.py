from pjml.config.description.cs.containercs import ContainerCS
from pjml.tool.model import Model
from pjml.tool.abc.transformer import Transformer
from pjml.tool.abc.nonconfigurablecontainer1 import NonConfigurableContainer1


class ApplyUsing(NonConfigurableContainer1):
    """Run a 'use' step right after an 'apply' one.

    Useful to calculate training error in classifiers, which would otherwise
    return PhantomData in the 'apply' step."""

    def __new__(cls, *args, transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            return object.__new__(cls)
        return ContainerCS(ApplyUsing.name, ApplyUsing.path, transformers)

    def _apply_impl(self, data):
        model = self.transformer.apply(data, self._exit_on_error)
        output_data = model.use(data, self._exit_on_error)
        return Model(output_data, model.use, self)

    def transformations(self, step=None, training_data=None):
        if training_data is None:
            training_data = self._last_training_data
        return self.transformer.transformations('u', training_data)
