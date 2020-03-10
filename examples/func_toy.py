from pjml.pipeline import Pipeline
from pjml.tool.data.communication.report import Report
from pjml.tool.data.flow.file import File
from pjml.tool.data.manipulation.keep import Keep
from pjml.tool.data.modeling.supervised.classifier.dt import DT
from pjml.tool.data.modeling.supervised.classifier.nb import NB

pipe = Pipeline(File("iris.arff"), NB(), Report('z'))
# pipe = Pipeline(File("iris.arff"), Keep(NB()), Report('z'), DT(), Report('z'))

model = pipe.apply()
print(1111111111111111, model)
d2 = model.use() #own_data=True)

print(11111111111111, d2)
