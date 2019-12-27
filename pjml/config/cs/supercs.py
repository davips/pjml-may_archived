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

    def __init__(self, name, path, config_space, nodes=None):
        super().__init__(name, path, nodes)
        self.config_space = config_space

    def sample(self):
        config = {'transformer': self.config_space.sample()}

        # Fill config with values from internal nodes.
        child_node = choice(self.nodes)
        config.update(child_node.partial_sample())

        return materialize(self.name, self.path, config)

    def updated(self, **kwargs):
        dic = {
            'name': self.name,
            'path': self.path,
            'config_space': self.config_space,
            'nodes': self.nodes
        }
        dic.update(kwargs)
        return self.__class__(**dic)
