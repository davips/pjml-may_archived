from pjml.config.cs.supercs import SuperCS
from pjml.tool.common.containern import ContainerN


def multi(*args, components=None):
    if components is None:
        components = args
    return SuperCS(Multi.name, Multi.path, components)


class Multi(ContainerN):
    """Process each Data object from a collection with its respective
    transformer."""

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
