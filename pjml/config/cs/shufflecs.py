import numpy as np
from pjml.config.cs.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.tool.data.container.seq import Seq


class ShuffleCS(ConfigSpace):
    """

    Parameters
    ----------
    config_spaces
        List of CSs. A permutation is sampled.
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
        css = self.config_spaces.copy()
        np.random.shuffle(css)
        return Seq(transformers=[cs.sample() for cs in css])
