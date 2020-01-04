from pjml.tool.base.seq import Seq


class Wrap(Seq):
    @property
    def wrapped(self):
        return self
