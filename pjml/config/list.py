from pjml.config.finiteconfigspace import FiniteConfigSpace
from pjml.tool.data.container.seq import Seq
from pjml.tool.data.evaluation.split import Split


def bag(*transformers):
    """Make a FiniteConfigSpace from a sequence of transformers."""
    return FiniteConfigSpace(nested=transformers)


def concat(*transformers):
    """Make a FiniteConfigSpace from a sequence of transformers."""
    return FiniteConfigSpace(nested=transformers)


def fetch(path):
    pass


def switch():
    pass


def sampler(split_type='cv', steps=10, test_size=0.3, seed=0, fields=None):
    """Make a FiniteConfigSpace with a sequence of Data splitters."""
    if fields is None:
        fields = ['X', 'Y']
    transformers = []
    for i in range(steps):
        transformers.append(
            Split(split_type, steps, i, test_size, seed, fields).transformer
        )
    return FiniteConfigSpace(nested=transformers)
