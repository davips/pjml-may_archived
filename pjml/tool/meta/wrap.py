from pjml.config.description.cs.containercs import ContainerCS
from pjml.config.description.cs.chaincs import ChainCS
from pjml.tool.abc.nonconfigurablecontainer1 import NonConfigurableContainer1
from pjml.tool.abc.transformer import Transformer
from pjml.util import flatten


class Wrap(NonConfigurableContainer1):
    def __new__(cls, *args, transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            return object.__new__(cls)
        return ContainerCS(Wrap.name, Wrap.path, transformers)

    def _apply_impl(self, data):
        self.model = self.transformer
        return self.transformer.apply(data)

    def _use_impl(self, data):
        return self.transformer.use(data)

    @property
    def wrapped(self):
        return self

    def transformations(self, step=None, training_data=None):
        if step is None:
            step = self._current_step
        # if training_data is None:
        #     training_data = self._last_training_data
        lst = []
        for tr in self.transformers:
            lst.append(tr.transformations(step, training_data))
        return flatten(lst)
