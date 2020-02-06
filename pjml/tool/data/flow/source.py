from cururu.storer import Storer
from pjdata.data import NoData
from pjml.tool.abc.transformer_nodata import Transformer_NoData


class Source(Transformer_NoData, Storer):
    """Source of Data object from a storage like MySQL, Pickle files, ...

    The first data object named 'name*' without transformations will be
    retrieved.

    #TODO: componente para recuperar resultados de transformação?
            Já seria o Cache?"""

    def __init__(self, name, fields=None, engine='dump', settings=None):
        if fields is None:
            fields = ['X', 'Y']
        if settings is None:
            settings = {}
        config = self._to_config(locals())

        self._set_storage(engine, settings)
        lst = self.storage.list_by_name(name)
        if len(lst) == 0:
            raise Exception(f'{name} dataset not found!')
        phantom_data = lst[0]
        data = self.storage.fetch(phantom_data, fields=fields)
        if data is None:
            raise Exception('Dataset not found: ', phantom_data.name)
        self.model = self.data = data
        super().__init__(config, self.data, deterministic=True)

    def _apply_impl(self, data):
        if data is not NoData:
            raise Exception('Source component needs to be applied with NoData. '
                            'Use Sink before it if needed.')
        return self.data

    def _use_impl(self, data):
        if data is not NoData:
            raise Exception('Source component needs to be used with NoData. '
                            'Use Sink before it if needed.')
        return self.data

    @classmethod
    def _cs_impl(cls):
        params = {
            'path': FixedP('./'),
            'name': FixedP('iris.arff')
        }
        return ComponentCS(Node(params=params))

    # def _transformations(self):
    #     """Source is a very special case of component.
    #
    #     It creates a history for the Data object from SGBD, so the expected
    #     list of transformations should come from there also."""
    #     if self._current_step == 'a':
    #         return [Apply(self)]
    #     else:
    #         return [Use(self, self._last_training_data)]
