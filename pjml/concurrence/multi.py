from pjml.base.component import Component


class Multi(Component):
    """Process each Data object from a collection with its respective
    transformer of the given FiniteConfigSpace."""

    def __init__(self, cs):
        self._configure(locals())
        # TODO: seed
        # TODO: aceitar componentes instanciados? = problemas de referências?
        #  desmaterializar?
        self.algorithm = cs
        self.size = self.algorithm.size

    def _apply_impl(self, collection):
        if not collection.infinite and self.size != collection.size:
            raise Exception('Config space and collection should have the same '
                            f'size {self.size} != collection {collection.size}')
        self.model = []
        datas = []
        for transformer in self.algorithm:
            component = transformer.materialize()
            data = component.apply(next(collection))
            datas.append(data)
            self.model.append(component)
        return collection.updated(self.transformation(), datas)

    def _use_impl(self, collection):
        if not collection.infinite and self.size != collection.size:
            raise Exception('Config space and collection should have the same '
                            f'size {self.size} != collection {collection.size}')
        datas = []
        for component in self.model:
            data = component.use(next(collection))
            datas.append(data)
        return collection.updated(self.transformation(), datas)

    @classmethod
    def _cs_impl(cls):
        raise Exception('It is not clear whether Multi should have a CS now.')

