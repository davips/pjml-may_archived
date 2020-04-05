from abc import ABC

from pjml.tool.abc.container import Container


class ContainerN(Container, ABC):
    """Container for more than one transformer."""

    def __init__(self, config, transformers):
        super().__init__(config, transformers)

        self.size = len(transformers)
