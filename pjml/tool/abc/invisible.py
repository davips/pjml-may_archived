from abc import ABC

from pjml.tool.base.transformer import Transformer


class Invisible(Transformer, ABC):
    """Parent class of all atomic transformers that don't increase history
    of transformations.

    They are useful, but sometimes do not transform Data objects."""

    def _transformations(self, step=None, training_data=None):
        """Invisible components produce no transformations, so they need to
        override the list of expected transformations with []."""
        return []
