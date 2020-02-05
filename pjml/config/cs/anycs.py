from pjml.config.cs.configspace import ConfigSpace


class AnyCS(ConfigSpace, set):
    """

    Parameters
    ----------
    config_spaces
        Set of CSs. Only one is sampled.
    """

    def __init__(self, *components):
        set.__init__(self, components)

    def sample(self):
        from pjml.config.distributions import choice
        cs = choice(list(self))

        # cs.cs ensures it is not a class or transformer.
        return cs.cs.sample()


