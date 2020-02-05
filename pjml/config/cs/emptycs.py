from pjml.config.cs.configspace import ConfigSpace
from pjml.tool.base.mixin.serialization import materialize


class EmptyCS(ConfigSpace, list):
    """CS for a component without settings, usually a NoOp.

    Parameters
    ----------
    name
        Name (usually the Python class) of the component.
    path
        Path (usually the Python module) of the component.
    """

    def __init__(self, name=None, path=None):
        list.__init__(self, [f'{name}@{path}'])  # For pretty printing.

        self.name = name
        self.path = path

    def sample(self):
        return materialize(self.name, self.path, {})

    def identified(self, name, path):
        return self.__class__(name=name, path=path)
