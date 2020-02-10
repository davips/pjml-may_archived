from pjml.config.description.cs.configspace import ConfigSpace


class SelectCS(ConfigSpace):
    """

    Parameters
    ----------
    components
        List of CSs. Only one is sampled.
    """

    def __init__(self, *components):
        components = [compo.cs for compo in components]
        super().__init__(cs='select', components=components)
        self.components = components

    def sample(self):
        from pjml.config.description.distributions import choice
        cs = choice(self.components)
        return cs.sample()
