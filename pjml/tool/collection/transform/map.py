from pjml.config.cs.containercs import ContainerCS
from pjml.tool.common.nonconfigurablecontainer1 import NonConfigurableContainer1


def mapa(*args, components=None):
    if components is None:
        components = args
    return ContainerCS(Map.name, Map.path, components)


class Map(NonConfigurableContainer1):
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
        return collection.updated(self._transformations(), datas=datas)

    def _use_impl(self, collection):
        size = len(self.model)
        if size != collection.size:
            raise Exception('Collections passed to apply and use should have '
                            f'the same size a- {size} != u- {collection.size}')
        datas = []
        for transformer in self.model:
            data = transformer.use(next(collection), self._exit_on_error)
            datas.append(data)
        return collection.updated(self._transformations(), datas=datas)
    # TODO: which containers should pass self._exit_on_error to transformer?
