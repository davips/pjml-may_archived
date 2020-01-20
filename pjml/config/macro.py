"""
Shortcuts of common pipelines.
"""
from pjml.config.list import split
from pjml.tool.base.seq import seq
from pjml.tool.collection.expand.expand import Expand
from pjml.tool.collection.reduce.summ import Summ
from pjml.tool.collection.transform.map import mapa
from pjml.tool.collection.transform.multi import multi


def evaluate(*components, sampler=split(partitions=10), function='mean_std'):
    return seq(
        Expand,
        multi(*sampler),
        mapa(components=components),
        Summ(function=function)
    )
