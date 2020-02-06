from pjml.tool.seq import Seq


class Wrap(Seq):
    @property
    def wrapped(self):
        return self
