from pjdata.aux.serialization import materialize
from pjml.config.description.cs.abc.configspace import ConfigSpace
from pjml.config.description.distributions import choice
from pjml.config.description.node import Node


class ContainerCS(ConfigSpace):
    """

    Parameters
    ----------
    components
        Multiple CS.
    """

    def __init__(self, name, path, components, *nodes):
        jsonable = {'component': {'name': name, 'path': path}, 'nodes': nodes}
        if components:
            components = [compo.cs for compo in components]
            jsonable['components'] = components
        super().__init__(jsonable)
        if any([not isinstance(cs, Node) for cs in nodes]):
            raise Exception('ContainerCS can only have Node as nodes.')
        self.name, self.path, self.nodes = name, path, nodes
        self.components = components

    def _sample_cfg(self):
        return {'transformers': [c.sample() for c in self.components]}

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
        return self.__class__(name, path, self.components, *self.nodes)
