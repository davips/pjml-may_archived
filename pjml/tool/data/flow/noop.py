from abc import ABC

from pjml.tool.data.flow.configless import ConfigLess


class NoOp(ConfigLess, ABC):
    """Parent class of all inert transformers.

    They are useful, but do nothing to Data objects."""
