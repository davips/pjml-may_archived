from pjml.config.description.cs.configspace import ConfigSpace


class ShuffleCS(ConfigSpace):
    """

    Parameters
    ----------
    components
        List of CSs. A permutation is sampled.
    """

    def __init__(self, *components):
        components = [compo.cs for compo in components]
        super().__init__(cs='shuffle', components=components)
        self.components = components

    def sample(self):
        import numpy as np
        from pjml.tool.seq import Seq
        css = self.components.copy()
        np.random.shuffle(css)
        return Seq(transformers=[cs.sample() for cs in css])
