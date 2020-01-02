import json
from abc import abstractmethod


class ConfigSpace:
    """Tree representing a (probably infinite) set of (hyper)parameter spaces.
    """

    @abstractmethod
    def sample(self):
        pass

    @property
    def cs(self):
        """Shortcut to ease retrieving a CS from a Transformer class without
        having to check that it is not already a CS."""
        return self

    def __str__(self):
        return json.dumps(self, sort_keys=False, indent=3)
