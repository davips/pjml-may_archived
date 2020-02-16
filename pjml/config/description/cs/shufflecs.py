from pjml.config.description.cs.abc.operatorcs import OperatorCS


class ShuffleCS(OperatorCS):
    """A permutation is sampled."""

    def sample(self):
        import numpy as np
        from pjml.tool.chain import Chain
        css = self.components.copy()
        np.random.shuffle(css)
        return Chain(transformers=[cs.sample() for cs in css])
