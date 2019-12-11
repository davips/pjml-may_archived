from pjml.config.finiteconfigspace import FiniteConfigSpace


def bag(transformers):
    """Make a FiniteConfigSpace from a sequence of transformers."""
    return FiniteConfigSpace(nested=transformers)


def sampler(transformers):
    """Make a FiniteConfigSpace with a sequence of Data splitters."""
    return FiniteConfigSpace(nested=transformers)

