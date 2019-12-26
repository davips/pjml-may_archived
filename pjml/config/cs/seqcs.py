import numpy as np
from pjml.config.cs.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.tool.data.container.seq import Seq


class SeqCS(ConfigSpace):
    """

    Parameters
    ----------
    config_spaces
        List of CSs. A Seq is sampled.
    """

    def __init__(self, config_spaces):
        self.config_spaces = [] if config_spaces is None else config_spaces

    def updated(self, **kwargs):
        dic = {
            'config_spaces': self.config_spaces
        }
        dic.update(kwargs)
        return self.__class__(**dic)

    def sample(self):
        transformers = [cs.sample() for cs in self.config_spaces]
        return Seq.cs(transformers=transformers)
