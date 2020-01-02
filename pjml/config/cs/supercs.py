from pjml.config.cs.componentcs import ComponentCS
from pjml.config.cs.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.tool.base.aux.serialization import materialize


class SuperCS(ComponentCS):
    """

    Parameters
    ----------
    config_space
        A single CS.
    """

    def __init__(self, config_space, *nodes, name=None, path=None):
        super().__init__(*nodes, name=name, path=path)
        self.config_space = config_space

    def sample(self):
        config = {'transformer': self.config_space.sample()}

        # Fill config with values from internal nodes.
        child_node = choice(self.nodes)
        config.update(child_node.partial_sample())

        return materialize(self.name, self.path, config)

    def identified(self, name, path):
        return self.__class__(config_space=self.config_space, *self.nodes,
                              name=name, path=path)
