from pjml.config.cs.seqcs import SeqCS
from pjml.tool.common.containern import ContainerN
from pjml.util import flatten


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
            data = transformer.apply(data, self._exit_on_error)
            if data and (data.failure is not None):
                raise Exception(
                    f'Applying subtransformer {transformer} failed! ',
                    data.failure)
        return data

    def _use_impl(self, data):
        for transformer in self.transformers:
            data = transformer.use(data, self._exit_on_error)
            if data and (data.failure is not None):
                raise Exception(f'Using subtransformer {transformer} failed! ',
                                data.failure)
        return data

    def _transformations(self, step=None, training_data=None):
        if step is None:
            step = self._current_step
        if training_data is None:
            training_data = self._last_training_data
        lst = []
        for tr in self.transformers:
            lst.append(tr._transformations(step)) #, training_data))
        return flatten(lst)
