from cururu.persistence import DuplicateEntryException
from cururu.storer import Storer
from pjdata.data import Data
from pjdata.dataset import Dataset
from pjml.config.cs.componentcs import ComponentCS
from pjml.config.distributions import choice
from pjml.config.node import Node
from pjml.config.parameter import FixedP, CatP
from pjml.tool.base.transformer import Transformer


class Store(Transformer, Storer):
    """Store a Data object onto a storage like MySQL, Pickle files, ...
        as a new dataset (beware of the darkness!). It is a NoOp.

    """

    def __init__(self, name_apply, description_apply='',
                 name_use=None, description_use=None, fields=None,
                 engine='dump',
                 settings=None):
        if fields is None:
            fields = ['X', 'Y']
        if settings is None:
            settings = {}
        config = self._to_config(locals())

        self._set_storage(engine, settings)

        if name_use is None:
            name_use = name_apply
        if description_use is None:
            description_use = description_apply

        self.dataset_apply = Dataset(name_apply, description_apply)
        self.dataset_use = Dataset(name_use, description_use)
        self.model = f'{name_apply}-{name_use}-' \
                     f'{description_apply}-{description_use}'
        self.fields = fields

        super().__init__(config, self.model, deterministic=True)

    def _apply_impl(self, data):
        new_data = Data(
            self.dataset_apply, data.history, data.failure, **data.matrices
        )
        try:
            self.storage.store(new_data, fields=self.fields)
        except DuplicateEntryException as e:
            print(e)
        return data

    def _use_impl(self, data):
        new_data = Data(
            self.dataset_use, data.history, data.failure, **data.matrices
        )
        print(123123, new_data)
        try:
            self.storage.store(new_data, fields=self.fields)
        except DuplicateEntryException as e:
            print(e)
        return data

    @classmethod
    def _cs_impl(cls):
        params = {
            'engine': CatP(choice, items=['dump', 'mysql', 'sqlite']),
            'settings': FixedP({})
        }
        return ComponentCS(Node(params=params))
