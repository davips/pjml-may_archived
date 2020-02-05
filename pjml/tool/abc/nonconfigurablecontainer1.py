from abc import ABC

from pjml.tool.base.seq import Seq
from pjml.tool.abc.container import Container
from pjml.tool.abc.container1 import Container1


class NonConfigurableContainer1(Container1, ABC):
    """Container for a single transformer without config by itself."""

    def __init__(self, *args, transformers=None):
        if transformers is None:
            transformers = args
        if not transformers:
            raise Exception(
                f'A container ({self.name}) should have at least one '
                f'transformer!')

        # Container1(Seq(a,b,c)) should be equal Container1(a,b,c)
        if len(transformers) == 1 and isinstance(transformers, Seq):
            transformers = transformers[0].transformers

        super().__init__(transformers)

        if len(transformers) > 1:
            self.transformer = Seq(transformers=transformers)
        else:
            self.transformer = transformers[0]
