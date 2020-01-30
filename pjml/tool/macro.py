"""
Shortcuts of common ML pipelines.
"""
from pjml.config.list import split
from pjml.tool.base.seq import Seq
from pjml.tool.collection.expand.expand import Expand
from pjml.tool.collection.expand.partition import Partition
from pjml.tool.collection.reduce.summ import Summ
from pjml.tool.collection.transform.map import Map
from pjml.tool.collection.transform.multi import Multi


def evaluator(*transformers, function='mean_std', **validation_args):
    return Seq(
        Partition(**validation_args),
        Map(transformers=transformers),
        Summ(function=function)
    )
