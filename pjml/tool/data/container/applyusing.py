from pjml.tool.base.transformer import Transformer


class ApplyUsing(Transformer):
    """Run a 'use' step right after an 'apply' one.

    Useful to calculate training error in classifiers, which would otherwise
    return None in the 'apply' step."""

    def __init__(self, transformer):
        super().__init__({'transformer': transformer}, transformer, True)
        self.model = self.algorithm
        self.transformer = transformer

    def _apply_impl(self, data):
        self.transformer.apply(data)
        return self.transformer.use(data)

    def _use_impl(self, data):
        return self.transformer.use(data)

    @classmethod
    def _cs_impl(cls):
        pass
