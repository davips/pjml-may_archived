from pjml.config.description.cs.configspace import ConfigSpace


class SeqCS(ConfigSpace, tuple):
    """Tuple of CSs.

    Parameters
    ----------

        A Seq is sampled.
    """

    def __new__(cls, *components):
        return tuple.__new__(SeqCS, components)

    def sample(self):
        # cs.cs ensures it is not a class or transformer.
        transformers = [cs.cs.sample() for cs in self]
        from pjml.tool.seq import Seq
        return Seq(transformers=transformers)
