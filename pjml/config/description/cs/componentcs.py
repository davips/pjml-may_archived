from pjdata.aux.serialization import materialize
from pjml.config.description.cs.emptycs import EmptyCS
from pjml.config.description.distributions import choice
from pjml.config.description.node import Node


class ComponentCS(EmptyCS):
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
        super().__init__(name, path)
        self.update({'cs': 'component', 'nodes': nodes})
        self.nodes = nodes
        if any([not isinstance(cs, Node) for cs in self.nodes]):
            raise Exception('CompleteCS can only have Nodes as children.')

    def _sample_cfg(self):
        return {}

    def sample(self):
        """Sample a completely configured transformer.

        Choose a path from tree and set values to parameters according to
        the given sampling functions.

        Returns
        -------
        A transformer
        """
        config = self._sample_cfg()

        # Fill config with values from internal nodes.
        if self.nodes:
            child_node = choice(self.nodes)
            config.update(child_node.partial_sample())

        return materialize(self.name, self.path, config)

    def identified(self, name, path):
        return self.__class__(*self.nodes, name=name, path=path)
