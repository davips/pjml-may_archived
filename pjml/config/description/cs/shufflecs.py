from pjml.config.description.cs.configspace import ConfigSpace


class ShuffleCS(ConfigSpace, list):
    """

    Parameters
    ----------
    config_spaces
        List of CSs. A permutation is sampled.
    """

    def __init__(self, *components):
        # Check if this is a CS-cursed built-in.
        if 'sample' in dir(components):
            # Ensure only CS objects are present.
            components = [compo.cs for compo in components]

        list.__init__(self, components)

    def sample(self):
        import numpy as np
        from pjml.tool.seq import Seq
        css = self.copy()
        np.random.shuffle(css)
        return Seq(transformers=[cs.sample() for cs in css])
