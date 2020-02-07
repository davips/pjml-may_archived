from pjml.config.description.cs.configspace import ConfigSpace


class SeqCS(ConfigSpace, tuple):
    """Tuple of CSs.

    Parameters
    ----------

        A Seq is sampled.
    """

    def __new__(cls, *components):
        # Ensures only CS objects are present.
        components = [comp.cs for comp in components]

        return tuple.__new__(SeqCS, components)

    def sample(self):
        transformers = [cs.sample() for cs in self]
        from pjml.tool.seq import Seq
        return Seq(transformers=transformers)
