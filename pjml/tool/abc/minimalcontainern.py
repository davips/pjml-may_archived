from abc import ABC

from pjml.tool.abc.container import Container
from pjml.tool.abc.containern import ContainerN


class MinimalContainerN(ContainerN, ABC):
    """Container for more than one transformer."""

    def __init__(self, *args, transformers=None, seed=0):
        if transformers is None:
            transformers = args
        super().__init__({'seed': seed}, transformers)
