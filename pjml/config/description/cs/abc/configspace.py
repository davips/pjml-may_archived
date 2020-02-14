from abc import abstractmethod

from pjdata.mixin.printable import Printable


class ConfigSpace(Printable):
    """Tree representing a (probably infinite) set of (hyper)parameter spaces.
    """

    def __init__(self, jsonable):
        jsonable.update(cs=self.__class__.__name__[0:-2].lower())
        super().__init__(jsonable)

    @abstractmethod
    def sample(self):
        pass

    @property
    def cs(self):
        """Shortcut to ease retrieving a CS from a Transformer class without
        having to check that it is not already a CS."""
        return self
