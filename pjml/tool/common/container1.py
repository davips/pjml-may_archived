from abc import ABC

from pjml.tool.base.seq import Seq
from pjml.tool.common.container import Container


class Container1(Container, ABC):
    """Container for a single transformer.

    If more are given, they will be handled as a single Seq transformer."""

    def __init__(self, *args, transformers=None):
        if transformers is None:
            transformers = args

        # Container1(Seq(a,b,c)) should be equal Container1(a,b,c)
        if len(transformers) == 1 and isinstance(transformers, Seq):
            transformers = transformers[0].transformers

        super().__init__({'transformers': transformers}, transformers)

        if len(transformers) > 1:
            self.transformer = Seq(transformers=transformers)
        else:
            self.transformer = transformers[0]
