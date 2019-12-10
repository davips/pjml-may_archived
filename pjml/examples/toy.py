from base.pipeline import Pipeline
from data_creation import read_arff
from evaluation.metric import Metric
from flow.report import Report
from modelling.supervised.classifier.dt import DT
from modelling.supervised.classifier.nb import NB
from processing.instance.sampler.over.rnd_over_sampler import RndOverSampler

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
