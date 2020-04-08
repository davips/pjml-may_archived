from pjml.config.description.cs.containercs import ContainerCS
from pjml.tool.abc.minimalcontainer import MinimalContainer1
from pjml.tool.abc.transformer import Transformer
from pjml.tool.model import Model


class ApplyUsing(MinimalContainer1):
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
        applied = model.use(data, exit_on_error=self._exit_on_error)
        return model.updated(self, data_after_apply=applied)
        # print(model._use_impl)
        # return Model(self, data, applied, use_impl=model._use_impl)

    def _use_impl(self, data, *args):
        print(45545454545454545, self.transformer.name)
        pass

    def transformations(self, step, clean=True):
        return self.transformer.transformations('u', clean)
