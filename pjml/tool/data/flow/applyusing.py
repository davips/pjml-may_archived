from pjml.config.cs.supercs import SuperCS
from pjml.tool.collection.transform.map import Container1


def au(*args, components=None):
    if components is None:
        components = args
    return SuperCS(ApplyUsing.name, ApplyUsing.path, components)


class ApplyUsing(Container1):
    """Run a 'use' step right after an 'apply' one.

    Useful to calculate training error in classifiers, which would otherwise
    return None in the 'apply' step."""

    def _apply_impl(self, data):
        self.transformer.apply(data, self._exit_on_error)
        self.model = self.transformer
        return self.transformer.use(data, self._exit_on_error)

    def _use_impl(self, data):
        return self.transformer.use(data, self._exit_on_error)
