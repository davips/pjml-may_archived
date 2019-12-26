from pjml.tool.base.transformer import Transformer


class Seq(Transformer):
    """Chain the execution of the given transformers.

    Each arg is a transformer. Optionally, a list of them can be passed as a
    named arg 'transformers'."""

    def __init__(self, *args, transformers=None):
        if transformers is None:
            transformers = args
        super().__init__({'transformers': transformers}, transformers)
        # TODO: seed

    def _apply_impl(self, data):
        self.model = self.algorithm
        for transformer in self.algorithm:
            data = transformer.apply(data)
            if data and (data.failure is not None):
                raise Exception(f'Applying subtransformer {transformer} failed! ',
                                data.failure)
        return data

    def _use_impl(self, data):
        for transformer in self.algorithm:
            data = transformer.use(data)
            if data and (data.failure is not None):
                raise Exception(f'Using subtransformer {transformer} failed! ',
                                data.failure)
        return data

    @classmethod
    def _cs_impl(cls):
        raise Exception('Seq has no CS! Use seq() operator.')
        # TODO: Seq pode ter CS com arg "config_spaces",
        #  mas pode haver uma função  atalho seq() pra isso.

    def cs(self, *args, transformers=None):
        pass
