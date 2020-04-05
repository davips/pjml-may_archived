from pjdata.finitecollection import FiniteCollection

from pjml.config.description.cs.containercs import ContainerCS
from pjml.tool.abc.minimalcontainer import MinimalContainerN
from pjml.tool.abc.transformer import Transformer
from pjml.tool.model import ContainerModel


class Multi(MinimalContainerN):
    """Process each Data object from a collection with its respective
    transformer."""

    def __new__(cls, *args, transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            return object.__new__(cls)
        return ContainerCS(Multi.name, Multi.path, transformers)

    def _apply_impl(self, collection_apply):
        isfinite = isinstance(collection_apply, FiniteCollection)
        if isfinite and self.size != collection_apply.size:
            raise Exception(
                f'Config space and collection should have the same size '
                f'{self.size} != collection {collection_apply.size}'
            )
        models = []
        datas = []
        for transformer in self.transformers:
            model = transformer.apply(
                next(collection_apply), self._exit_on_error
            )
            datas.append(model.data)
            models.append(model)

        applied = collection_apply.updated(
            self.transformations('a'), datas=datas
        )
        return ContainerModel(self, collection_apply, applied, models)

    def _use_impl(self, collection_use, models=None):
        isfinite = isinstance(collection_use, FiniteCollection)
        if isfinite and self.size != collection_use.size:
            raise Exception(
                'Config space and collection should have the same '
                f'size {self.size} != collection {collection_use.size}'
            )
        datas = []
        for model in models:
            data = model.use(next(collection_use), self._exit_on_error)
            datas.append(data)
        return collection_use.updated(self.transformations('u'),
                                      datas=datas)
