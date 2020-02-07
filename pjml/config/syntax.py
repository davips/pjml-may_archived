from forbiddenfruitinit import curse, reverse

from pjml.config.description.cs.selectcs import SelectCS
from pjml.config.description.cs.seqcs import SeqCS
from pjml.config.description.cs.shufflecs import ShuffleCS


def enable():
    """
    Override Python built-ins for a cleaner AutoML expression syntax.

    Warning: this changes globally the types: list, set and tuple.
    Call disable() to revert this, or use enable() only on scripts.

    This just adds some methods (sample, cs) to them,
    so it is not a big concern.

    Eg. selecting classifiers:
    expr = NR, PCA, {SVM, MLP}

    Eg. shuffling preprocessors:
    expr = [NR, PCA], {SVM, MLP}
    """
    curse(list, "sample", ShuffleCS.sample)
    curse(set, "sample", SelectCS.sample)
    curse(tuple, "sample", SeqCS.sample)

    curse(list, "cs", ShuffleCS.cs)
    curse(set, "cs", SelectCS.cs)
    curse(tuple, "cs", SeqCS.cs)

    curse(list, "__init__", ShuffleCS.__init__)
    curse(set, "__init__", SelectCS.__init__)
    curse(tuple, "__init__", SeqCS.__init__)
    print('WARNING: The expression short syntax has been enabled!')


def disable():
    """Disable global effects of the special AutoML expression syntax."""
    reverse(list, "sample")
    reverse(set, "sample")
    reverse(tuple, "sample")

    reverse(list, "cs")
    reverse(set, "cs")
    reverse(tuple, "cs")

    reverse(list, "__init__")
    reverse(set, "__init__")
    reverse(tuple, "__init__")
    print('WARNING: The expression short syntax has been disabled!')
