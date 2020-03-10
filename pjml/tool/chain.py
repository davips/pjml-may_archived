from pjml.config.description.cs.chaincs import ChainCS
from pjml.tool.abc.containern import ContainerN
from pjml.tool.abc.transformer import Transformer
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
        models = []
        for transformer in self.transformers:
            print(transformer.name)
            model = transformer.apply(data, self._exit_on_error)
            data = model.data
            models.append(model)
            if data and data.failure is not None:
                print(f'Applying subtransformer {transformer} failed! ',
                      data.failure)
                return data, self._no_use_impl

        def use_impl(data_):
            for model_ in models:
                print(transformer.name)
                data_ = model_.use(data_, self._exit_on_error)
                if data_ and data_.failure is not None:
                    print(f'Using submodel {model_} failed! ', data_.failure)
                    return data_
            return data_

        return data, use_impl

    def __str__(self, depth=''):
        if not self._pretty_printing:
            return super().__str__()

        txts = []
        for t in self.transformers:
            txts.append(t.__str__(depth))
        return '\n'.join(txts)
