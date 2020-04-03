from pjml.config.description.cs.chaincs import ChainCS
from pjml.tool.abc.containern import ContainerN
from pjml.tool.abc.transformer import Transformer
from pjml.tool.model import Model, ContainerModel
from pjml.util import flatten


class Chain(ContainerN):
    """Chain the execution of the given transformers.

    Each arg is a transformer. Optionally, a list of them can be passed as a
    named arg called 'transformers'."""

    def __new__(cls, *args, transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            return object.__new__(cls)
        return ChainCS(*transformers)

    def _apply_impl(self, data):
        before_data = data
        models = []
        for transformer in self.transformers:
            model = transformer.apply(data, self._exit_on_error)
            data = model.data
            models.append(model)
            if data and data.failure:
                print(f'Applying subtransformer {transformer} failed! ',
                      data.failure)
                return ContainerModel(self, before_data, data, models,
                                      use_impl=self._use_for_failed_pipeline)

        return ContainerModel(self, before_data, data, models)

    def _use_impl(self, data, models=None):
        for model in models:
            data = model.use(data, self._exit_on_error)
            if data and data.failure:
                print(f'Using submodel {model} failed! ', data.failure)
                break
        return data

    def __str__(self, depth=''):
        if not self._pretty_printing:
            return super().__str__()

        txts = []
        for t in self.transformers:
            txts.append(t.__str__(depth))
        return '\n'.join(txts)
