from pjml.config.description.cs.configspace import ConfigSpace


class SeqCS(ConfigSpace, tuple):
    """Tuple of CSs.

    Parameters
    ----------

        A Seq is sampled.
    """

    def __new__(cls, *components):
        # Ensures only CS objects are present.
        components = [compo.cs for compo in components]
        return tuple.__new__(SeqCS, components)

    def sample(self):
        # cs.cs only needed when using short syntax
        transformers = [cs.cs.sample() for cs in self]
        from pjml.tool.seq import Seq
        return Seq(transformers=transformers)
