from abc import abstractmethod

from pjml.config.distributions import choice
from pjml.config.transformer import Transformer


class ConfigSpace:
    """Tree representing a (probably infinite) set of (hyper)parameter spaces.
    """

    @abstractmethod
    def sample(self):
        pass

    @abstractmethod
    def updated(self):
        pass


