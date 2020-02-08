from pjml.config.description.cs.configspace import ConfigSpace


class SelectCS(ConfigSpace, list):
    """

    Parameters
    ----------
    config_spaces
        List of CSs. Only one is sampled.
    """

    def __init__(self, *components):
        # Ensure only CS objects are present (mostly for pretty printing).
        components = [compo.cs for compo in components]

        list.__init__(self, components)

    def sample(self):
        from pjml.config.description.distributions import choice
        cs = choice(self)
        return cs.sample()


