from pjml.config.description.cs.configspace import ConfigSpace


class SelectCS(ConfigSpace, set):
    """

    Parameters
    ----------
    config_spaces
        Set of CSs. Only one is sampled.
    """

    def __init__(self, *components):
        # Ensures only CS objects are present.
        components = [cs.cs for cs in components]

        set.__init__(self, components)

    def sample(self):
        from pjml.config.description.distributions import choice
        cs = choice(list(self))
        return cs.sample()


