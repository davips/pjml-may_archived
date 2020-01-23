from pjml.config.cs.componentcs import ComponentCS
from pjml.config.node import Node
from pjml.config.parameter import FixedP
from pjml.tool.common.invisible import Invisible


class Save(Invisible):

    def __init__(self, name, path='./'):
        config = self._to_config(locals())
        if not path.endswith('/'):
            raise Exception('Path should end with /', path)
        if name.endswith('arff'):
            filename = path + name
        else:
            raise Exception('Unrecognized file extension:', name)
        super().__init__(config, filename, deterministic=True)
        self.model = filename
        self.filename = filename

    def _apply_impl(self, data):
        pass

    def _use_impl(self, data):
        pass

    @classmethod
    def _cs_impl(cls):
        params = {
            'path': FixedP('./'),
            'name': FixedP('iris.arff')
        }
        return ComponentCS(Node(params=params))
