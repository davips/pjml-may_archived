from pjml.config.description.cs.abc.componentcs import ComponentCS


class ContainerCS(ComponentCS):
    """

    Parameters
    ----------
    components
        Multiple CS.
    """

    def __init__(self, name, path, components, *nodes):
        super().__init__(name, path, components, *nodes)

    def _sample_cfg(self):
        return {'transformers': [c.sample() for c in self.components]}

    def identified(self, name, path):
        return self.__class__(name, path, self.components, *self.nodes)
