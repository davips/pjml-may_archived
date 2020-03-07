from pjml.tool.data.flow.file import File
from pjml.tool.data.modeling.supervised.classifier.nb import NB

d = File("iris.arff").apply().data

m = NB().apply(d)
d2 = m.use(d)

print(11111111111111, d2)
