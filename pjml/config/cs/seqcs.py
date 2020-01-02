from pjml.config.cs.configspace import ConfigSpace


class SeqCS(ConfigSpace, tuple):
    """

    Parameters
    ----------
    config_spaces
        Tuple of CSs. A Seq is sampled.
    """

    def __new__(cls, *components):
        return tuple.__new__(SeqCS, *components)

    def sample(self):
        # cs.cs ensures it is not a class or transformer.
        transformers = [cs.cs.sample() for cs in self]
        from pjml.tool.base.seq import Seq
        return Seq(transformers=transformers)
