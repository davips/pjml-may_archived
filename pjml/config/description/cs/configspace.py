import json
import traceback
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
        #TODO: TypeError: Object of type ABCMeta is not JSON serializable
        try:
            return json.dumps(self, sort_keys=False, indent=4)
        except Exception as e:
            print('Problems printing:', self.__class__.__name__)
            traceback.print_exc()
            exit(0)
