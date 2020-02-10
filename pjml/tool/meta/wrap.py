from pjml.config.description.cs.containercs import ContainerCS
from pjml.config.description.cs.seqcs import SeqCS
from pjml.tool.abc.nonconfigurablecontainer1 import NonConfigurableContainer1
from pjml.tool.abc.transformer import Transformer


class Wrap(NonConfigurableContainer1):
    def __new__(cls, *args, transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            instance = NonConfigurableContainer1.__new__(Wrap)
            instance.__init__(transformers=transformers)
            # instance = NonConfigurableContainer1.__new__(
            #     Wrap, transformers=transformers
            # )
            # TODO: checar se precisa mesmo de init() em todos os new()
            return instance
        return ContainerCS(Wrap.name, Wrap.path, transformers)

    def _apply_impl(self, data):
        self.model = self.transformer
        return self.transformer.apply(data)

    def _use_impl(self, data):
        return self.transformer.use(data)

    @property
    def wrapped(self):
        return self

    # def __str__(self, depth=''):
    #     from pjml.tool.abc.containern import ContainerN
    #     return super(ContainerN).__str__()
