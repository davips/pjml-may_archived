from abc import ABC

from pjml.tool.abc.transformer import Transformer1


class SKLAlgorithm(Transformer1, ABC):
    """    Base class for scikitlearn algorithms.    """

    def __init__(self, config, algorithm_factory, deterministic=False):
        super().__init__(config, deterministic)
        self.algorithm_factory = algorithm_factory
