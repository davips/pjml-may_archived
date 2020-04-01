from abc import ABC

from pjml.tool.abc.transformer import HeavyTransformer


class Algorithm(HeavyTransformer, ABC):
    """    Base class for scikitlearn algorithms.    """

    def __init__(self, config, algorithm_factory, deterministic=False):
        super().__init__(config, deterministic)
        self.algorithm_factory = algorithm_factory
