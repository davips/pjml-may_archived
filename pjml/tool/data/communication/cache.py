import traceback

from cururu.storer import Storer
from pjdata.operation.apply import Apply
from pjdata.operation.use import Use
from pjml.config.cs.supercs import SuperCS
from pjml.config.node import Node
from pjml.config.parameter import FixedP
from pjml.tool.base.seq import Seq
from pjml.tool.base.singleton import NoModel
from pjml.tool.common.container import Container


def cache(*args, engine="dump", settings=None, components=None):
    if components is None:
        components = args
    """Shortcut to create a ConfigSpace for Cache."""
    node = Node(params={'engine': FixedP(engine), 'settings': FixedP(settings)})
    return SuperCS(Cache.name, Cache.path, components, node)


class Cache(Container, Storer):
    def __init__(self, *args, fields=None, engine="dump", settings=None,
                 transformers=None):
        if settings is None:
            settings = {}
        if transformers is None:
            transformers = args

        # Cache(Seq(a,b,c)) should be equal to Cache(a,b,c)
        if len(transformers) == 1 and isinstance(transformers, Seq):
            transformers = transformers[0].transformers

        # TODO: propagar seed
        config = self._to_config(locals())
        config['transformers'] = transformers
        self.transformers = transformers
        del config['args']

        if fields is None:
            fields = ['X', 'Y', 'Z']

        # TODO: generalize this (as ConfigurableContainer) to future components.
        # Bypass to Container due to specific config of Cache.
        super(Container, self).__init__(config, transformers)

        if len(transformers) > 1:
            self.transformer = Seq(transformers=transformers)
        else:
            self.transformer = transformers[0]

        self.fields = fields
        self._set_storage(engine, settings)

    def _apply_impl(self, data):
        # TODO: CV() is too cheap to be recovered from storage, specially if
        #  it is a LOO. Maybe transformers could inform whether they are cheap.
        transformation = Apply(self.transformer)
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
            try:
                output_data = self.transformer.apply(data, exit_on_error=False)
            except:
                self.storage.unlock(data, transformation)
                traceback.print_exc()
                exit(0)

            data_to_store = data.phantom if output_data is None else output_data
            self.storage.store(
                data_to_store,
                data, transformation,
                self.fields,
                check_dup=False
            )

        self.model = NoModel if self.transformer.model is None \
            else self.transformer.model  # TODO: <-- entender e comentar isso

        return output_data

    def _use_impl(self, data):
        # exit(0)
        transformation = Use(self.transformer, self._last_training_data)
        output_data = self.storage.fetch(
            data, transformation, self.fields,
            lock=True
        )

        # Use if still needed  ----------------------------------
        if output_data is None:
            # If the component was applied (probably simulated by storage),
            # but there is no model, we reapply it...
            if self.transformer.model is None:
                # Melhor deixar quebrar caso um
                # apply() seja armazenado e o use() correspondente não?
                # Ou guardar referência pro conjunto de treino para reinduzir?
                # Fazer dump do transformer resolve melhor, mas pode ser
                # custoso.
                # Usuário pode decidir, escolhendo um cache local para isso.
                print('It is possible that a previous apply() was successfully'
                      ' stored, but use() with current data wasn\'t.\n'
                      'E.g. you are trying to use in new data, or use() never '
                      'was stored before.\n')
                print('Recovering training data from transformer to reapply it.'
                      'The goal is to induce a model usable by use()...\n'
                      f'comp: {self.transformer.sid} '
                      f'data: {data.sid}'
                      f'training data: {self._last_training_data}')
                # stored_train_data = self.storage.fetch(train_uuid)
                self.transformer.apply(self._last_training_data)

            try:
                output_data = self.transformer.use(data, exit_on_error=False)
            except:
                self.storage.unlock(data, transformation)
                traceback.print_exc()
                exit(0)

            data_to_store = data.phantom if output_data is None else output_data
            self.storage.store(
                data_to_store,
                data, transformation, self.fields,
                check_dup=False
            )

        return output_data
