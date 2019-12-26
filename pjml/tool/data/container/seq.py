from pjml.tool.base.component import Component


class Seq(Component):
    """Chain the execution of the given components.

    Each arg is a component. Optionally, a list of them can be passed as a
    named arg 'components'."""

    def __init__(self, *args, components=None):
        if components is None:
            components = args
        super().__init__({'components': components}, components)
        # TODO: seed
        # TODO: auto dematerialize component into transformer?

    def _apply_impl(self, data):
        self.model = self.algorithm
        for component in self.algorithm:
            data = component.apply(data)
            if data and (data.failure is not None):
                raise Exception(f'Applying subcomponent {component} failed! ',
                                data.failure)
        return data

    def _use_impl(self, data):
        for component in self.algorithm:
            data = component.use(data)
            if data and (data.failure is not None):
                raise Exception(f'Using subcomponent {component} failed! ',
                                data.failure)
        return data

    @classmethod
    def _cs_impl(cls):
        raise Exception('Seq has no CS! Use seq() operator.')
        # TODO: Seq pode ter CS com arg "config_spaces",
        #  mas pode haver uma função  atalho seq() pra isso.

    def cs(self, *args, components=None):
        pass
