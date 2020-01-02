from abc import abstractmethod

from pjml.config.cs.componentcs import ComponentCS


class SuperCS(ComponentCS):
    """Abstract class for SuperCSs."""

    def __init__(self, name, path, cs_or_css, *nodes):
        super().__init__(*nodes, name=name, path=path)
        self.config_space = cs_or_css
        self.config_spaces = cs_or_css

        self.append(cs_or_css)  # For pretty printing.

    @abstractmethod
    def _sample_cfg(self):
        pass


class Super1CS(SuperCS):
    """

    Parameters
    ----------
    config_space
        Single CS.
    """

    def __init__(self, name, path, config_space, *nodes):
        super().__init__(name, path, config_space, *nodes)

    def _sample_cfg(self):
        return {'transformer': self.config_space.cs.sample()}


class SuperNCS(SuperCS):
    """

    Parameters
    ----------
    config_space
        Multiple CS.
    """

    def __init__(self, name, path, config_space, *nodes):
        super().__init__(name, path, config_space, *nodes)

    def _sample_cfg(self):
        return {'transformers': [c.cs.sample() for c in self.config_spaces]}
