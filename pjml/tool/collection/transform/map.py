from pjml.config.description.cs.containercs import ContainerCS
from pjml.tool.abc.transformer import Transformer
from pjml.tool.abc.nonconfigurablecontainer1 import NonConfigurableContainer1
from pjdata.infinitecollection import InfiniteCollection

from pjml.tool.model import ContainerModel


class Map(NonConfigurableContainer1):
    """Execute the same transformer for the entire collection."""

    def __new__(cls, *args, transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            return object.__new__(cls)
        return ContainerCS(Map.name, Map.path, transformers)

    def _apply_impl(self, collection):
        if isinstance(collection, InfiniteCollection):
            raise Exception('Collection should be finite for Map!')
        models = []
        datas = []
        for data in collection:
            transformer = self.transformer.clone()
            model = transformer.apply(data, self._exit_on_error)
            datas.append(model.data)
            models.append(transformer) # dar append no output_data?
    
        def use_impl(collection):
            size = len(models)
            if size != collection.size:
                raise Exception('Collections passed to apply and use should have '
                                f'the same size a- {size} != u- {collection.size}')
            datas = []
            for model in models:
                data = model.use(next(collection), self._exit_on_error)
                datas.append(data)
            return collection.updated(self.transformations(step='u'), datas=datas)
        # TODO: which containers should pass self._exit_on_error to transformer?

        applied = collection.updated(self.transformations(step='a'), datas=datas)

        return ContainerModel(models, applied, self, use_impl)
