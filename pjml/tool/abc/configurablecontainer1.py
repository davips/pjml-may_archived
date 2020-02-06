from abc import ABC

from pjml.tool.abc.container import Container
from pjml.tool.abc.container1 import Container1
from pjml.tool.seq import Seq


class ConfigurableContainer1(Container1, ABC):
    """Configurable container for a single transformer.

    If more are given, they will be handled as a single Seq transformer."""

    def __init__(self, config):
        transformers = config['transformers']
        if not transformers:
            raise Exception('A container should have at least one transformer!')

        # ConfigurableContainerXXX(Seq(a,b,c)) should be equal to
        # ConfigurableContainerXXX(a,b,c)
        if len(transformers) == 1 and isinstance(transformers, Seq):
            transformers = transformers[0].transformers

        # Bypass Container init.
        super(Container, self).__init__(config, transformers)

        self.transformers = transformers
        if len(transformers) > 1:
            self.transformer = Seq(transformers=transformers)
        else:
            self.transformer = transformers[0]

