import numpy as np
from pjml.config.cs.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.tool.base.transformer import Transformer
from pjml.tool.data.container.seq import Seq, seq


class SuperCS(ConfigSpace):
    """

    Parameters
    ----------
    config_space
        A single CS.
    """

    def __init__(self, name, path, config_space):
        self.name = name
        self.path = path
        self.config_space = config_space

    def updated(self, **kwargs):
        dic = {
            'name': self.name,
            'path': self.path,
            'config_space': self.config_space
        }
        dic.update(kwargs)
        return self.__class__(**dic)

    def sample(self):
        config = {'transformer': self.config_space.sample()}
        return Transformer.materialize(self.name, self.path, config)
