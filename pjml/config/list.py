"""
Module to create CS from transformers.
"""


def concat(*transformers):
    # TODO: para que era isso msm?
    pass


def fetch(path):
    pass


def switch():
    pass


def sampler(split_type='cv', steps=10, test_size=0.3, seed=0, fields=None):
    """Make a sequence of Data splitters."""
    from pjml.tool.data.evaluation.split import Split
    if fields is None:
        fields = ['X', 'Y']
    transformers = []
    for i in range(steps):
        s = Split(split_type, steps, i, test_size, seed, fields)
        transformers.append(
            Split(split_type, steps, i, test_size, seed, fields)
        )
    # from pjml.config.cs.finitecs import FiniteCS
    # return FiniteCS(trasformers=transformers).sample()
    return tuple(transformers)

# def bag(*transformers):
#     """Make a FiniteConfigSpace from a sequence of transformers."""
#     # from pjml.config.cs.finitecs import FiniteCS
#     # return FiniteCS(trasformers=transformers)
#     return transformers
