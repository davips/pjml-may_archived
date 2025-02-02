from abc import ABC

from pjml.tool.abc.container import Container


class ContainerN(Container, ABC):
    """Container for more than one transformer."""

    def __init__(self, config, seed, transformers, deterministic):
        super().__init__(config, seed, transformers, deterministic)

        self.size = len(transformers)
