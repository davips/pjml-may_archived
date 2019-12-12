from pjml.base.component import Component


class Map(Component):
    """Execute the same transformer/component for the entire collection."""

    def __init__(self, element):
        if isinstance(element, Component):
            element = element.transformer
        self._configure(locals())
        # TODO: seed
        self.algorithm = element

    def _apply_impl(self, collection):
        if collection.infinite:
            raise Exception('Collection should be finite for Map!')
        self.model = []
        datas = []
        for data in collection:
            component = self.algorithm.materialize()
            output_data = component.apply(data)
            datas.append(output_data)
            self.model.append(component)
        return collection.updated(self.transformation(), datas)

    def _use_impl(self, collection):
        size = len(self.model)
        if size != collection.size:
            raise Exception('Collections passed to apply and use should have '
                            f'the same size a- {size} != u- {collection.size}')
        datas = []
        for component in self.model:
            data = component.use(next(collection))
            datas.append(data)
        return collection.updated(self.transformation(), datas)

    @classmethod
    def _cs_impl(cls):
        raise Exception('It is not clear whether Multi should have a CS now.')
