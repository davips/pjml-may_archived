from pjml.tool.base.transformer import Transformer


class Multi(Transformer):
    """Process each Data object from a collection with its respective
    transformer."""

    def __init__(self, transformers):
        # TODO: propagar seed
        # TODO: testar se cs é finito?
        super().__init__({'transformers': transformers}, transformers)
        self.size = len(transformers)
        self.transformers = transformers

    def _apply_impl(self, collection):
        if not collection.infinite and self.size != collection.size:
            raise Exception('Config space and collection should have the same '
                            f'size {self.size} != collection {collection.size}')
        self.model = []
        datas = []
        # TODO: deve clonar antes de usar?
        for transformer in self.transformers:
            data = transformer.apply(next(collection))
            datas.append(data)
            self.model.append(transformer)
        return collection.updated1(self._transformation(), datas=datas)

    def _use_impl(self, collection):
        if not collection.infinite and self.size != collection.size:
            raise Exception('Config space and collection should have the same '
                            f'size {self.size} != collection {collection.size}')
        datas = []
        for transformer in self.model:
            data = transformer.use(next(collection))
            datas.append(data)
        return collection.updated1(self._transformation(), datas=datas)

    @classmethod
    def _cs_impl(cls):
        raise Exception('Multi should have a CS:'
                        'Pode ter um finiteCS de tamanho um (se for passado 1 '
                        'finiteCS) ou pode ter um CS combinando vários CS '
                        'passados')
