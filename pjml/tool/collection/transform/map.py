from pjml.config.cs.supercs import SuperCS
from pjml.tool.common.container1 import Container1


def mapa(*args, components=None):
    if components is None:
        components = args
    return SuperCS(Map.name, Map.path, components)


class Map(Container1):
    """Execute the same transformer for the entire collection."""

    def _apply_impl(self, collection):
        if collection.infinite:
            raise Exception('Collection should be finite for Map!')
        self.model = []
        datas = []
        for data in collection:
            transformer = self.transformer.clone()
            output_data = transformer.apply(data, self._exit_on_error)
            datas.append(output_data)
            self.model.append(transformer)
        return collection.updated(self._transformation(), datas=datas)

    def _use_impl(self, collection):
        size = len(self.model)
        if size != collection.size:
            raise Exception('Collections passed to apply and use should have '
                            f'the same size a- {size} != u- {collection.size}')
        datas = []
        for transformer in self.model:
            data = transformer.use(next(collection), self._exit_on_error)
            datas.append(data)
        return collection.updated(self._transformation(), datas=datas)
