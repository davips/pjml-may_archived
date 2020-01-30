from pjml.config.cs.containercs import ContainerCS
from pjml.tool.base.transformer import Transformer
from pjml.tool.common.containern import ContainerN


class Multi(ContainerN):
    """Process each Data object from a collection with its respective
    transformer."""
    def __new__(cls, *args, transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            return ContainerN.__new__(Multi)
        return ContainerCS(Multi.name, Multi.path, transformers)

    def _apply_impl(self, collection):
        if not collection.infinite and self.size != collection.size:
            raise Exception('Config space and collection should have the same '
                            f'size {self.size} != collection {collection.size}')
        self.model = []
        datas = []
        # TODO: deve clonar antes de usar?
        for transformer in self.transformers:
            data = transformer.apply(next(collection), self._exit_on_error)
            datas.append(data)
            self.model.append(transformer)
        return collection.updated(self._transformations(), datas=datas)

    def _use_impl(self, collection):
        if not collection.infinite and self.size != collection.size:
            raise Exception('Config space and collection should have the same '
                            f'size {self.size} != collection {collection.size}')
        datas = []
        for transformer in self.model:
            data = transformer.use(next(collection), self._exit_on_error)
            datas.append(data)
        return collection.updated(self._transformations(), datas=datas)
