"""
Shortcuts of common CS/AutoML pipelines.
"""
from pjml.tool.base.seq import Seq
from pjml.tool.collection.expand.partition import Partition
from pjml.tool.collection.reduce.summ import Summ
from pjml.tool.collection.transform.map import Map


def evaluator(*components, function='mean_std', **validation_args):
    return Seq(
        Partition(**validation_args),
        Map(transformers=components),
        Summ(function=function)
    )
