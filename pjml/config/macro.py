"""
Shortcuts of common CS/AutoML pipelines.
"""
from pjml.config.list import split
from pjml.tool.base.seq import seq
from pjml.tool.collection.expand.expand import Expand
from pjml.tool.collection.expand.partition import Partition
from pjml.tool.collection.reduce.summ import Summ
from pjml.tool.collection.transform.map import mapa
from pjml.tool.collection.transform.multi import multi


def evaluator(*components, function='mean_std', **validation_args):
    return seq(
        Partition(**validation_args),
        mapa(components=components),
        Summ(function=function)
    )
