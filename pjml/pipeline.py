class Pipeline:
    """Chain the execution of the given components."""

    def __init__(self, *args):
        self.components = args

    def apply(self, data):
        for component in self.components:
            data = component.apply(data)
            if data and (data.failure is not None):
                raise Exception(f'Applying subcomponent {component} failed! ',
                                data.failure)
        return data

    def use(self, data):
        for component in self.components:
            data = component.use(data)
            if data and (data.failure is not None):
                raise Exception(f'Using subcomponent {component} failed! ',
                                data.failure)
        return data
