from pjml.config.cs.configspace import ConfigSpace


class ShuffleCS(ConfigSpace, list):
    """

    Parameters
    ----------
    config_spaces
        List of CSs. A permutation is sampled.
    """

    def __init__(self, *components):
        list.__init__(self, components)

    def sample(self):
        import numpy as np
        from pjml.tool.base.seq import Seq
        css = self.copy()
        np.random.shuffle(css)
        return Seq(transformers=[cs.cs.sample() for cs in css])


class Shuffle(ShuffleCS):
    pass
