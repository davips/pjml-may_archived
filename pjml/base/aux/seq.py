from pjml.base.component import Component
from pjml.config.configspace import ConfigSpace


class Seq(Component):
    """Chain the execution of the given components."""

    def __init__(self, *args, components=None):
        if components is None:
            components = args
        self._configure(locals())
        # TODO: seed
        # TODO: auto dematerialize component into transformer?
        self.algorithm = components

    def _apply_impl(self, data):
        for component in self.algorithm:
            data = component.apply(data)
            if data.failure is not None:
                raise Exception(f'Applying subcomponent {component} failed! ',
                                data.failure)
        return data

    def _use_impl(self, data):
        for component in self.algorithm:
            data = component.use(data)
            if data.failure is not None:
                raise Exception(f'Using subcomponent {component} failed! ',
                                data.failure)
        return data

    @classmethod
    def _cs_impl(cls):
        raise Exception('Seq has no CS! Use seq() operator.')
