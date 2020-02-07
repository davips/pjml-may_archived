from pjdata.aux.serialization import materialize
from pjml.config.description.cs.configspace import ConfigSpace


class EmptyCS(ConfigSpace, dict):
    """CS for a component without settings, usually a NoOp.

    Parameters
    ----------
    name
        Name (usually the Python class) of the component.
    path
        Path (usually the Python module) of the component.
    """

    def __init__(self, name=None, path=None):
        # For pretty printing.
        dict.__init__(self, {'type': 'EmptyCS', 'transf': f'{name}@{path}'})

        self.name = name
        self.path = path

    def sample(self):
        return materialize(self.name, self.path, {})

    def identified(self, name, path):
        return self.__class__(name=name, path=path)
