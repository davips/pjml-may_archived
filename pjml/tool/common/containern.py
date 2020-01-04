from abc import ABC

from pjml.tool.common.container import Container


class ContainerN(Container, ABC):
    """Container for more than one transformer."""

    def __init__(self, *args, transformers=None):
        if transformers is None:
            transformers = args
        # TODO: propagar seed
        super().__init__({'transformers': transformers}, transformers)

        self.transformers = transformers
        self.size = len(transformers)
