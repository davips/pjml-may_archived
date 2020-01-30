"""
Overrides of python built-ins for an pajé expression cleaner syntax

Use:
   import pjml.config.syntax

Warning: this changes the types list, set and tuple globally.
However, this just adds the method sample() to them, so it is not a big concern.

Eg.:
expr = NR, PCA, {SVM, MLP}

Eg. shuffling preprocessors:
expr = [NR, PCA], {SVM, MLP}
"""
from forbiddenfruit import curse

from pjml.config.cs.anycs import AnyCS
from pjml.config.cs.seqcs import SeqCS
from pjml.config.cs.shufflecs import ShuffleCS

curse(list, "sample", ShuffleCS.sample)
curse(set, "sample", AnyCS.sample)
curse(tuple, "sample", SeqCS.sample)

curse(list, "cs", ShuffleCS.cs)
curse(set, "cs", AnyCS.cs)
curse(tuple, "cs", SeqCS.cs)
