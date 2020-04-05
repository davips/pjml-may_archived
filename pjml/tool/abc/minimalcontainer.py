from abc import ABC

from pjml.tool.abc.container1 import Container1
from pjml.tool.abc.containern import ContainerN


class Minimalist:
    """Mixin to provide 'init' with minimum configuration (seed)."""

    def __init__(self, *args, transformers=None, seed=0):
        if transformers is None:
            transformers = args
        self._super.__init__(self, {}, seed, transformers, deterministic=True)
        # TODO: Until now, every MinimalContainer is deterministic.
        #  Every container propagates the seed to the config of its internal
        #  transformers. So, it is determinist per se. However,
        #  a MinimalContainer that is randomized in some way may appear in
        #  the future.


class MinimalContainer1(Minimalist, Container1, ABC):
    """Container with minimum configuration (seed) for a single transformer.

    If more are given, they will be handled as a single Chain transformer."""
    _super = Container1


class MinimalContainerN(Minimalist, ContainerN, ABC):
    """Container with minimum configuration (seed) for more than one
    transformer."""
    _super = ContainerN
