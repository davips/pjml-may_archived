from cururu.file import save
from pjdata.data_creation import read_arff
from pjml.pipeline import Pipeline
from pjml.tool.base.seq import Seq
from pjml.tool.data.evaluation.metric import Metric
from pjml.tool.data.communication.report import Report
from pjml.tool.data.communication.cache import Cache
from pjml.tool.data.flow.ausing import ApplyUsing
from pjml.tool.data.flow.file import File
from pjml.tool.data.modeling.supervised.classifier.dt import DT
from pjml.tool.data.modeling.supervised.classifier.nb import NB
from pjml.tool.data.modeling.supervised.classifier.svmc import SVMC
from pjml.tool.data.processing.instance.sampler.over.random import ROS
from pjml.tool.macro import evaluator

# ML 1 ========================================================================
# datain = File('iris.arff').apply()
pipe = Pipeline(
    File('iris.arff'),
    evaluator(
        Cache(
            Seq(
                ApplyUsing(
                    SVMC(kernel='linear')
                ),
                Cache(Metric(function='accuracy')),
            ),
        )
    ),
    Report("{history.last.config['function']} $S for dataset {dataset.name}.")
)

print('--------', pipe.serialized)
save('/tmp/pipe', pipe)
#
# pipe = load('/tmp/pipe')
# print(pipe)

print(1111111111111111111111111111111)
dout = pipe.apply()
save('/tmp/pipea', pipe)
print(222222222222222222222222222221)
dout = pipe.use()
print(3333333333333333333333333333333)


# ML 2 ========================================================================
pipe = Pipeline(
    File('iris.arff'),

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

1
Antes era LEVEZA E 4 NÍVEIS - COM DEFEITO NO USE
Transformation(transformer, op)
Transformer(name, path, config)
Component(config)
Component
Containers conteriam outros transformers em config.
pros: basicamente dicts de strings = sem referências = menos memória
cons: havia o Component para o mesmo conceito, mas materializado

2
Agora é PESO E 3 NÍVEIS - COM DEFEITO NO USE
Transformation(transformer, op)
Transformer(config)  <-  equivale a component e transformer
Transformer
pros: conceitualmente mais simples
cons: transformer (e indiretamente transformation) agora inclui modelo,
        então referências a transformer mantém a memória mais ocupada.
        Se o Data tiver vida curta ou for gerado em poucas quantidades não há 
        problema, especialmente porque nada é copiado (structural sharing).
      do histórico do Data é possível puxar um transformer e reutilizar, 
      ou seja, outros datas que referenciem ele não podem contar com a 
      imutabilidade do modelo
        
3
Pode ficar: 1 OU 2 - COM CONSERTO DA AMBIGUIDADE DA TRANSFORMATION EM USE
ApplyTrantion(transformer, op) / UseTrantion(transformer, training_data, op) 
Transformer(config)
Transformer
pros: conserta o problema de que diferentes treinos produziam diferentes 
        use-transformations com a mesma identidade
cons: mesmos de 1 ou de 2

4
Pode ficar: ABOLIR REFERÊNCIAS, ADOTAR SÓ UUID
applyuuid=(transfuuid, op) / useuuid=(transfuuid, training_datauuid, op) 
Transformer(config)
Transformer
pros: leve, sem referências e mantém meta de identificação única de Data
cons: corta o cordão umbilical data-transformações, mas alguém quer saber as 
        transformações, ou basta o pipeline?

5
Adaptar 4: MANTÉM TRANSFORMATIONAPP E TRANSFORMATIONUSE, MAS SÓ ARMAZENA EM 
    BANCO SE O USUÁRIO PEDIR
pros: meio termo
cons: volta referências ou volta divisão entre conceitos component/transformer

"""
