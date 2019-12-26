class Pipeline:
    """Chain the execution of the given transformers."""

    def __init__(self, *args):
        self.transformers = args

    def apply(self, data):
        for transformer in self.transformers:
            data = transformer.apply(data)
            if data and (data.failure is not None):
                raise Exception(f'Applying subtransformer {transformer} failed! ',
                                data.failure)
        return data

    def use(self, data):
        for transformer in self.transformers:
            data = transformer.use(data)
            if data and (data.failure is not None):
                raise Exception(f'Using subtransformer {transformer} failed! ',
                                data.failure)
        return data
