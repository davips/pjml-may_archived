from pjml.config.cs.supercs import Super1CS
from pjml.tool.collection.transform.map import Container1


def apus(component):
    return Super1CS(ApplyUsing.name, ApplyUsing.path, component)


class ApplyUsing(Container1):
    """Run a 'use' step right after an 'apply' one.

    Useful to calculate training error in classifiers, which would otherwise
    return None in the 'apply' step."""

    def _apply_impl(self, data):
        self.transformer.apply(data)
        self.model = self.transformer
        return self.transformer.use(data)

    def _use_impl(self, data):
        return self.transformer.use(data)
