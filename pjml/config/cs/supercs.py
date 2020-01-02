from pjml.config.cs.componentcs import ComponentCS
from pjml.config.distributions import choice
from pjml.tool.base.aux.serialization import materialize


class SuperCS(ComponentCS):
    """

    Parameters
    ----------
    config_spaces
        Single or multiple CSs.
    """

    def __init__(self, name, path, config_spaces, *nodes):
        super().__init__(*nodes, name=name, path=path)
        self.config_spaces = config_spaces

        self.append(config_spaces)  # For pretty printing.


    def sample(self):
        if len(self.config_spaces) > 1:
            cfg = {'transformers': [c.cs.sample() for c in self.config_spaces]}
        else:
            cfg = {'transformer': self.config_spaces[0].cs.sample()}

        # Fill config with values from internal nodes.
        child_node = choice(self.nodes)
        cfg.update(child_node.partial_sample())

        return materialize(self.name, self.path, cfg)
