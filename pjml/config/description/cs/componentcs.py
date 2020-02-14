from pjml.config.description.cs.containercs import ContainerCS
from pjml.config.description.node import Node


class ComponentCS(ContainerCS):
    """Complete settings for a component (a component is a set of
    transformers, e.g. the component KNN represents the set of all k-NN
    transformers: KNN(k=1), KNN(k=3), ...

    Parameters
    ----------
    nodes
        List of internal nodes. Only one is sampled at a time.
    name
        Name (usually the Python class) of the component.
    path
        Path (usually the Python module) of the component.
    """

    def __init__(self, name=None, path=None, *nodes):
        super().__init__(name, path, components=None, *nodes)

    def _sample_cfg(self):
        return {}

    def identified(self, name, path):
        return self.__class__(name, path, *self.nodes)
