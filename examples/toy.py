import os
from pathlib import Path

from cururu.disk import save, load
from pjdata.fastdata import FastData
from pjml.config.list import sampler
from pjml.pipeline import Pipeline
from pjml.tool.base.seq import Seq
from pjml.tool.data.communication.cache import Cache
from pjml.tool.data.communication.report import Report
from pjml.tool.data.evaluation.metric import Metric
from pjml.tool.data.flow.applyusing import ApplyUsing
from pjml.tool.data.flow.file import File
from pjml.tool.data.flow.source import Source
from pjml.tool.data.modeling.supervised.classifier.dt import DT
from pjml.tool.data.modeling.supervised.classifier.nb import NB
from pjml.tool.data.modeling.supervised.classifier.svmc import SVMC
from pjml.tool.data.processing.instance.sampler.over.random import ROS
from pjml.tool.macro import evaluator
from pjdata import data
# data.Data = FastData

# # Armazenar dataset, sem depender do pacote pjml.
# from pjdata.data_creation import read_arff
# PickleServer().store(read_arff('iris.arff'))

# # Listar *iris*
# lst = PickleServer().list_by_name('iris')
# print(lst)

# # Armazenar dataset com gambiarrando no pjml.
# from pjml.tool.data.communication.cache import Cache
# from pjml.tool.data.flow.file import File
#
# Cache(File('iris.arff')).apply()

# ML 1 ========================================================================
datain = Source('iris.arff').apply()
from pjml.tool.meta.wrap import Wrap

# print(load('/tmp/dump/pipe').model)
# print()
# print(load('/tmp/dump/pipea').wrapped)
# Seq(File('abalone3.arff'), load('/tmp/dump/pipea')).use(datain)
# exit(0)

pipe = Pipeline(
    # File('abalone3.arff'),
    Source('iris'),
    evaluator(
        Cache(
            ApplyUsing(
                Wrap(SVMC(kernel='linear'))
            ),
            Metric(function='accuracy'),
            settings={'db': '/tmp/cururu'}
        )
    ),
    Report(" $S for dataset {dataset.name}.")
    # Report("{history.last.config['function']} $S for dataset {dataset.name}.")
)

# save('/tmp/dump/pipe0', pipe)


print('--------\n', pipe.serialized)
print('--------\n', pipe.wrapped.serialized)
save('/tmp/cururu/pipe', pipe)
#
# pipe = load('/tmp/pipe')
# print(pipe)

print(111111)
dout = pipe.apply()
save('/tmp/cururu/pipea', pipe)
print(222222)
dout = pipe.use()
print(333333)

# ML 2 ========================================================================
pipe = Pipeline(
    Source('iris.arff'),

    ROS(sampling_strategy='not minority'),

    ApplyUsing(NB('bernoulli')),
    Metric(function='accuracy'),
    # Report('Accuracy: $r {history}'),
    Report('Accuracy: $r'),

    ApplyUsing(DT(max_depth=2)),
    Metric(function='accuracy'),
    Report('Accuracy: $r'),

    ApplyUsing(SVMC(kernel='linear')),
    Metric(function='accuracy'),
    Report('Accuracy: $r'),
)
dataout = pipe.apply()
dataout2 = pipe.use()

# print(dataout.history)
# print(dataout2.history)

"""
Problemas filosoficos

obs. Containers sempre contêm referências a outros transformers (sejam leves ou 
pesados) em config.

obs. Um mesmo pipeline pode gerar diversos históricos. 
GA não pode confiar no histórico, pois as mutações podem fazer com que data 
seja alterado e mude o comportamento do pipeline (trocando transformations);
ou seja, o GA deve ocorrer sobre o pipeline, não sobre as trasformations;
melhor dizendo, sobre o transformer, não sobre transformations

1
Antes era LEVEZA E 4 NÍVEIS - COM DEFEITO NO USE
Transformation(transformer, op)
Transformer(name, path, config)
Component(config)
Component
pros: basicamente dicts de strings = sem referências = menos memória
cons: havia o Component para o mesmo conceito, mas materializado


Solução atual = 1 abaixo
Estratégia: comparar desempenho das três em tempo (com e sem cache) e memória.


1 gasta mais espaço e mantém referências

Apply(transformer) / Use(transformer, training_data) 
Transformer(config)     <-  equivale a component+transformer
Transformer             <-  atalho para CS



2 gasta menos espaço e não mantém referências, mas burocratiza um pouco... 
(otimização prematura?)

Apply(transformer.serialized) / Use(transformer.serialized, training_data.uuid) 
Transformer(config)     <-  equivale a component+transformer
Transformer             <-  atalho para CS

    obs. Transformation não precisa de Transformer dentro dele. Quem precisar 
    pode
            materializá-lo.



3 espaço zero e sem referências, mas sem histórico

aply: data.uuid = uuid(data.uuid + transformer.uuid)
use:  data.uuid = uuid(data.uuid + transformer.uuid + training_data.uuid) 
Transformer(config)     <-  equivale a component+transformer
Transformer             <-  atalho para CS


4 usuário decide entre 1, 2 e 3; configuração seria numa das seguintes formas:
    a. variável global HISTORY=full|text|zero
    b. arg no apply/use cascateado automaticamente  <-- preferida 1
    c. arg no Transformer.__init__                  <-- fracassa para automl
    d. monkey-patch pjdata.data com pjdata.fastdata <-- preferida 2



Monkey patch:
from pjdata.fastdata import FastData
from pjdata import data
data.Data = FastData

Com abalone3.arff e PickleServer-speed
full: 45s/1.5s 204M  (prov dump do Data está levando Transformers junto)
zero: 45s/1.5s 40M

Com abalone3.arff e PickleServer-space-blosc
full: Illegal instruction (core dumped) 
zero: 47s/1.5s 10M

Com abalone3.arff e PickleServer-space-mono
full: 46s/1.9s 48M 
zero: 46s/1.5s 10M

Transformer dump não guarda model porque só tem name,path,config no dict for 
json.
"""
