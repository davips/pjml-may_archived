from abc import abstractmethod


class ConfigSpace:
    """Tree representing a (probably infinite) set of (hyper)parameter spaces.
    """

    @abstractmethod
    def sample(self):
        pass

    @abstractmethod
    def updated(self):
        pass


