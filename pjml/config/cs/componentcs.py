from pjml.config.cs.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.config.node import Node
from pjml.tool.base.transformer import Transformer


class ComponentCS(ConfigSpace):
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

    def __init__(self, name, path, nodes):
        self.name = name
        self.path = path
        self.nodes = nodes
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

        return Transformer.materialize(self.name, self.path, config)

    def updated(self, **kwargs):
        dic = {
            'name': self.name,
            'path': self.path,
            'nodes': self.nodes
        }
        dic.update(kwargs)
        return self.__class__(**dic)
