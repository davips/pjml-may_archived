from abc import ABC

from pjml.tool.abc.container1 import Container1


class MinimalContainer1(Container1, ABC):
    """Container with minimum configuration (seed) for a single transformer.

    If more are given, they will be handled as a single Chain transformer."""

    def __init__(self, *args, transformers=None, seed=0):
        if transformers is None:
            transformers = args
        super().__init__({'seed': seed}, transformers)
