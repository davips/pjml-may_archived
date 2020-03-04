from pjml.config.description.cs.abc.operatorcs import OperatorCS


class SelectCS(OperatorCS):
    """Only one CS is sampled."""

    def sample(self):
        from pjml.config.description.distributions import choice
        cs = choice(self.components)
        print("CS ", cs)
        return cs.sample()
