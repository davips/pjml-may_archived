from pjml.config.cs.configspace import ConfigSpace
from pjml.config.distributions import choice


class AnyCS(ConfigSpace):
    """

    Parameters
    ----------
    config_spaces
        List of CSs. Only one is sampled.
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
        cs = choice(self.config_spaces)
        return cs.sample()
