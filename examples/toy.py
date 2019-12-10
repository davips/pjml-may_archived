from pjml.base.pipeline import Pipeline
from pjdata.data_creation import read_arff
from pjml.evaluation.metric import Metric
from pjml.flow.report import Report
from pjml.modelling.supervised.classifier.dt import DT
from pjml.modelling.supervised.classifier.nb import NB
from pjml.processing.instance.sampler.over.rnd_over_sampler import \
    RndOverSampler

datain = read_arff('iris.arff')
pipe = Pipeline(
    RndOverSampler(sampling_strategy='not minority'),

    NB('bernoulli'),
    Metric(function='accuracy'),
    Report('Accuracy: $r'),

    DT(max_depth=2),
    Metric(function='accuracy'),
    Report('Accuracy: $r'),
)
print(datain)
pipe.apply(datain)
dataout = pipe.use(datain)
print(dataout.r)
print('------------------')
print(DT.cs())
print('------------------')
print(DT.cs().sample())