from pjml.config.description.cs.containercs import ContainerCS
from pjml.config.description.node import Node
from pjml.config.description.parameter import FixedP
from pjml.tool.abc.configurablecontainer1 import ConfigurableContainer1


# def keep(*args, engine="dump", settings=None, components=None):
#     if components is None:
#         components = args
#     """Shortcut to create a ConfigSpace for Cache."""
#     node = Node(params={'engine': FixedP(engine), 'settings': FixedP(
#     settings)})
#     return SuperCS(Cache.name, Cache.path, components, node)
from pjml.tool.abc.transformer import Transformer


class Keep(ConfigurableContainer1):
    """Preserve original values of the given fields."""

    # TODO: implement __new__ to generate a CS

    def __new__(cls, *args, fields=None, transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            return object.__new__(cls)
        node = Node(params={'fields': FixedP(fields)})
        return ContainerCS(Keep.name, Keep.path, transformers, node)

    def __init__(self, *args, fields=None, transformers=None):
        if transformers is None:
            transformers = args
        if fields is None:
            fields = ['X', 'Y']
        config = self._to_config(locals())
        del config['args']
        super().__init__(config)

        self.fields = fields
        self.model = fields

    def _apply_impl(self, data):
        return self._step(self.transformer.apply, data)

    def _use_impl(self, data):
        return self._step(self.transformer.use, data)

    def _step(self, f, data):
        print(111111111111111111111111111, data.name)
        matrices = {k: data.field(k, self) for k in self.fields if k in data.matrices}
        new_matrices = f(data).matrices
        new_matrices.update(matrices)
        return data.updated(self.transformations(), **new_matrices)
