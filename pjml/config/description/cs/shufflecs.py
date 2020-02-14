from pjml.config.description.cs.abc.operatorcs import OperatorCS


class ShuffleCS(OperatorCS):
    """A permutation is sampled."""

    def sample(self):
        import numpy as np
        from pjml.tool.seq import Seq
        css = self.components.copy()
        np.random.shuffle(css)
        return Seq(transformers=[cs.sample() for cs in css])
