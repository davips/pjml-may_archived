from pjml.config.description.cs.configspace import ConfigSpace


class SeqCS(ConfigSpace):
    """Tuple of CSs.

    Parameters
    ----------

        A Seq is sampled.
    """
    def __init__(self, *components):
        components = [compo.cs for compo in components]
        super().__init__(cs='seq', components=components)
        self.components = components

    def sample(self):
        transformers = [cs.sample() for cs in self.components]
        from pjml.tool.seq import Seq
        return Seq(transformers=transformers)
