from pjml.config.description.cs.abc.operatorcs import OperatorCS


class SeqCS(OperatorCS):
    """A Seq is sampled."""

    def sample(self):
        transformers = [cs.sample() for cs in self.components]
        from pjml.tool.seq import Seq
        return Seq(transformers=transformers)
