from abc import ABC

from pjml.tool.abc.transformer import Transformer2


class Invisible(Transformer2, ABC):
    """Parent class of all atomic transformers that don't increase history
    of transformations.

    They are useful, but sometimes do not transform Data objects."""

    def transformations(self, step):
        """Invisible components produce no transformations, so they need to
        override the list of expected transformations with []."""
        return []
