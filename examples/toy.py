from pjdata.data_creation import read_arff
from pjml.base.aux.seq import Seq
from pjml.base.pipeline import Pipeline
from pjml.concurrence.expand import Expand
from pjml.concurrence.map import Map
from pjml.concurrence.multi import Multi
from pjml.concurrence.reduce.summ import Summ
from pjml.config.lists import sampler
from pjml.evaluation.metric import Metric
from pjml.flow.report import Report
from pjml.modelling.supervised.classifier.dt import DT
from pjml.modelling.supervised.classifier.nb import NB
from pjml.modelling.supervised.classifier.svmc import SVMC
from pjml.processing.instance.sampler.over.rnd_over_sampler import \
    RndOverSampler

datain = read_arff('iris.arff')
pipe = Pipeline(
    RndOverSampler(sampling_strategy='not minority'),

    NB('bernoulli'),
    Metric(function='accuracy'),
    Report('Accuracy: $r {history}'),

    DT(max_depth=2),
    Metric(function='accuracy'),
    Report('Accuracy: $r'),

    SVMC(kernel='linear'),
    Metric(function='accuracy'),
    Report('Accuracy: $r'),
)
# print(datain)
# dataout = pipe.apply(datain)
# dataout2 = pipe.use(datain)
#
# print(dataout.history)
# print(dataout2.history)
# print('------------------')
# print(SVMC.cs())
#
# print('------------------')
# print(SVMC.cs().sample())


pipe = Pipeline(Expand(),
                Multi(sampler('cv')),
                Map(Seq(
                    SVMC(kernel='linear'),
                    Metric(function='accuracy')
                )),
                Summ(),
                Report('Mean $s for dataset {dataset.name}.')
                )

pipe.apply(datain)