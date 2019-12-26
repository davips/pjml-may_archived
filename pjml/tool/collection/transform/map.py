from pjml.tool.base.transformer import Transformer


class Map(Transformer):
    """Execute the same transformer for the entire collection."""

    def __init__(self, transformer):
        # TODO: propagar seed
        super().__init__({'transformer': transformer}, transformer)

    def _apply_impl(self, collection):
        if collection.infinite:
            raise Exception('Collection should be finite for Map!')
        self.model = []
        datas = []
        for data in collection:
            transformer = self.algorithm.clone()
            output_data = transformer.apply(data)
            datas.append(output_data)
            self.model.append(transformer)
        return collection.updated(self.transformation(), datas)

    def _use_impl(self, collection):
        size = len(self.model)
        if size != collection.size:
            raise Exception('Collections passed to apply and use should have '
                            f'the same size a- {size} != u- {collection.size}')
        datas = []
        for transformer in self.model:
            data = transformer.use(next(collection))
            datas.append(data)
        return collection.updated(self.transformation(), datas)

    @classmethod
    def _cs_impl(cls):
        # TODO: CS
        raise Exception(
            'deve expor o CS do componente passado, mas dentro de um SuperCS')
