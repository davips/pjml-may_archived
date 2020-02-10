from pjml.config.description.cs.componentcs import ComponentCS


class ContainerCS(ComponentCS):
    """

    Parameters
    ----------
    components
        Multiple CS.
    """

    def __init__(self, name, path, components, *nodes):
        super().__init__(name=name, path=path, *nodes)
        components = [compo.cs for compo in components]
        self.update({'cs': 'container', 'components': components})
        self.components = components

    def _sample_cfg(self):
        return {'transformers': [c.sample() for c in self.components]}
