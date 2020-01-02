import json

from pjml.config.cs.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.config.node import Node
from pjml.tool.base.aux.serialization import materialize


class ComponentCS(ConfigSpace, list):
    """Complete settings for a component (a component is a set of
    transformers, e.g. the component KNN represents the set of all k-NN
    transformers: KNN(k=1), KNN(k=3), ...

    Parameters
    ----------
    name
        Name (usually the Python class) of the component.
    path
        Path (usually the Python module) of the component.
    nodes
        List of internal nodes. Only one is sampled at a time.
    """

    def __init__(self, *nodes, name=None, path=None):
        list.__init__(self, nodes)
        self.append(f'{name}@{path}')  # For pretty printing.

        self.nodes = nodes
        self.name = name
        self.path = path
        if any([not isinstance(cs, Node) for cs in self.nodes]):
            raise Exception('CompleteCS can only have Nodes as children.')

    def sample(self):
        """Sample a transformer completely configured.

        Choose a path from tree and set values to parameters according to
        the given sampling functions.

        Returns
        -------
        A transformer
        """
        config = {}

        # Fill config with values from internal nodes.
        child_node = choice(self.nodes)
        config.update(child_node.partial_sample())

        return materialize(self.name, self.path, config)

    def identified(self, name, path):
        return self.__class__(*self.nodes, name=name, path=path)
