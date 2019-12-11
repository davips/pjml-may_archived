from pjdata.data_creation import read_arff
from pjml.base.pipeline import Pipeline
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
print(datain)
dataout = pipe.apply(datain)
dataout2 = pipe.use(datain)

print(dataout.history)
print(dataout2.history)
# print('------------------')
# print(SVMC.cs())
#
# print('------------------')
# print(SVMC.cs().sample())
