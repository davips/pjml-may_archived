from pjml.config.description.cs.componentcs import ComponentCS


class ContainerCS(ComponentCS):
    """

    Parameters
    ----------
    config_spaces
        Multiple CS.
    """

    def __init__(self, name, path, config_spaces, *nodes):
        super().__init__(*nodes, name=name, path=path)
        self.config_spaces = config_spaces

        # For pretty printing.
        dict.__init__(self, {'type': 'ContainerCS', 'transf': name + '@' + path,
                             'CSs': config_spaces, 'nodes': nodes})

        def _sample_cfg(self):
            return {'transformers': [c.cs.sample() for c in self.config_spaces]}
