from pjml.config.cs.componentcs import ComponentCS


class SuperCS(ComponentCS):
    """

    Parameters
    ----------
    config_spaces
        Multiple CS.
    """

    def __init__(self, name, path, config_spaces, *nodes):
        super().__init__(*nodes, name=name, path=path)
        self.config_spaces = config_spaces

        self.append(config_spaces)  # For pretty printing.

    def _sample_cfg(self):
        return {'transformers': [c.cs.sample() for c in self.config_spaces]}
