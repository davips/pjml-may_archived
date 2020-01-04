from pjml.config.cs.seqcs import SeqCS
from pjml.tool.common.containern import ContainerN


def seq(*args, components=None):
    if components is None:
        components = args
    return SeqCS(*components)


class Seq(ContainerN):
    """Chain the execution of the given transformers.

    Each arg is a transformer. Optionally, a list of them can be passed as a
    named arg called 'transformers'."""

    def _apply_impl(self, data):
        self.model = self.transformers
        for transformer in self.transformers:
            data = transformer.apply(data)
            if data and (data.failure is not None):
                raise Exception(
                    f'Applying subtransformer {transformer} failed! ',
                    data.failure)
        return data

    def _use_impl(self, data):
        for transformer in self.transformers:
            data = transformer.use(data)
            if data and (data.failure is not None):
                raise Exception(f'Using subtransformer {transformer} failed! ',
                                data.failure)
        return data
