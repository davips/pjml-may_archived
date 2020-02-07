from pjml.config.description.cs.configspace import ConfigSpace


class SelectCS(ConfigSpace, set):
    """

    Parameters
    ----------
    config_spaces
        Set of CSs. Only one is sampled.
    """

    def __init__(self, *components):
        # Check if this is a CS-cursed built-in.
        if 'sample' in dir(components):
            # Ensure only CS objects are present.
            components = [compo.cs for compo in components]

        set.__init__(self, components)

    def sample(self):
        from pjml.config.description.distributions import choice
        cs = choice(list(self))
        return cs.sample()


