from functools import lru_cache

from cururu.amnesia import Amnesia
from cururu.pickleserver import PickleServer
from pjdata.transformation import Transformation
from pjml.config.distributions import choice
from pjml.config.node import Node
from pjml.config.parameter import CatP
from pjml.tool.base.transformer import Transformer
from pjml.tool.data.container.container import Container


def cache(component, engine="file", settings=None):
    """Shortcut to create a ConfigSpace for Cache.

    Parameters
    ----------
    component

    engine
    settings

    Returns
    -------

    """
    return Cache.cs(component, engine=engine, settings=settings)


class Cache(Container):
    def __init__(self, transformer, fields=None, engine="file", settings=None):
        if isinstance(fields, Transformer):
            raise Exception(
                f'Container {self.name} should have a single transformer!')

        if fields is None:
            fields = ['X', 'Y', 'Z']
        if settings is None:
            settings = {'db': '/tmp/'}

        super().__init__(
            transformer=transformer,
            config=self._to_config(locals())
        )

        self.fields = fields

        if engine == "amnesia":
            self.storage = Amnesia()
        elif engine == "mysql":
            from cururu.mysql import MySQL
            self.storage = MySQL(**settings)
        elif engine == "sqlite":
            from cururu.sqlite import SQLite
            self.storage = SQLite(**settings)
        elif engine == "cachedmysql":
            from cururu.mysql import MySQL
            from cururu.sqlite import SQLite
            self.storage = MySQL(db=settings['db'], nested=SQLite())
        elif engine == "file":
            self.storage = PickleServer(**settings)
        else:
            raise Exception('Unknown engine:', engine)

    def _apply_impl(self, data):
        # TODO: CV() is too cheap to be recovered from storage, specially if
        #  it is a LOO. Maybe transformers could inform whether they are cheap.
        transformation = Transformation(self.transformer, 'a')
        output_data = self.storage.fetch(
            data, transformation, self.fields,
            lock=True
        )
        # pra carregar modelo:
        # self.transformer = self.storage.fetch_transformer(
        #     data, self.transformer, lock=True
        # )
        #
        # pra guardar modelo:
        # self.storage.store_transformer(self.transformer, self.fields,
        #                                check_dup=True)

        # Apply if still needed  ----------------------------------
        if output_data is None:
            output_data = self.transformer.apply(data)
            data_to_store = data.phantom if output_data is None else output_data
            self.storage.store(
                data, transformation, self.fields,
                data_to_store,
                check_dup=False
            )

        return output_data

    def _use_impl(self, data):
        transformation = Transformation(self.transformer, 'u')
        output_data = self.storage.fetch(
            data, transformation, self.fields,
            lock=True
        )

        # Use if still needed  ----------------------------------
        if output_data is None:
            # If the component was applied (probably simulated by storage),
            # but there is no model, we reapply it...
            if self.transformer.model is None:
                # TODO: recover from apply-stored-but-use-not-stored.
                print('It is possible that a previous apply() was '
                      'successfully stored, but its use() wasn\'t.'
                      'Or you are trying to use in new data.')
                print(
                    'Trying to recover training data from storage to apply '
                    'just to induce a model usable by use()...\n'
                    f'comp: {self.transformer.sid}  data: {data.sid} ...')
                # stored_train_data = self.storage.fetch(train_uuid)
                # self.component.apply_impl(stored_train_data)

            output_data = self.transformer.use(data)
            data_to_store = data.phantom if output_data is None else output_data
            self.storage.store(
                data, transformation, self.fields,
                data_to_store,
                check_dup=False
            )

        return output_data

    @classmethod
    def _cs_impl(cls):
        params = {'engine': CatP(
            choice, items=["amnesia", "mysql", "sqlite", "nested"]
        )}  # TODO: cada engine é um ramo!
        return Node(params=params)

    @lru_cache()
    def to_transformations(self, operation):
        return self.transformer.to_transformations(operation)
