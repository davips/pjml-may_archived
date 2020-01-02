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

from pjdata.data_creation import read_arff
from pjml.config.cs.anycs import AnyCS
from pjml.config.cs.seqcs import SeqCS
from pjml.config.cs.shufflecs import ShuffleCS
from pjml.tool.data.modeling.supervised.classifier.dt import DT
from pjml.tool.data.modeling.supervised.classifier.nb import NB
from pjml.tool.data.processing.feature.scaler.minmax import MinMax
from pjml.tool.data.processing.feature.scaler.std import Std
from pjml.tool.data.processing.instance.sampler.over.rnd_over_sampler import ROS
from pjml.tool.data.processing.instance.sampler.under.rnd_under_sampler import \
    RUS

curse(list, "sample", ShuffleCS.sample)
curse(set, "sample", AnyCS.sample)
curse(tuple, "sample", SeqCS.sample)
curse(list, "cs", ShuffleCS.cs)
curse(set, "cs", AnyCS.cs)
curse(tuple, "cs", SeqCS.cs)