import traceback

from pjml.base.transformer import Transformer
from pjml.searchspace.distributions import choice


class ConfigSpace:
    """Tree representing a set of (hyper)parameter spaces.

        Parameters
        ----------
        name
            Name (usually the Python class) of the component.
        path
            Path (usually the Python module) of the component.
        params
            Dictionary like {'param1': Param(...), 'param2': Param(...), ...}.
        nested
            List of internal nodes. Only one is sampled.
        children
            List of the next nodes. Only one is sampled.
    """

    def __init__(self, name=None, path=None, params=None, nested=None,
                 children=None):
        self.name = name
        self.path = path
        self.params = {} if params is None else params
        self.nested = [] if nested is None else nested
        self.children = [] if children is None else children

    def updated(self, **kwargs):
        dic = {
            'name': self.name,
            'path': self.path,
            'params': self.params,
            'nested': self.nested,
            'children': self.children
        }
        dic.update(kwargs)
        return ConfigSpace(**dic)

    def sample(self):
        """Choose a path from tree and set values to parameters according to
        the given sampling functions.

        Sampling will return a list if it has children.
        """
        if self.iscomplete():
            config = {}

            # First, fill args with values from nested nodes.
            if self.nested:
                nested_node = choice(self.nested)
                config = nested_node.sample()
                config.update(config)

            # After, fill args with values from child nodes.
            child_node = self
            while child_node.children:
                child_node = choice(child_node.children)
                config = child_node.sample()
                config.update(config)

            # Then complete args with current node values, possibly overriding
            # some values from children/nested nodes (this happens with
            # frozen arguments given to cs(...)).
            for name, param in self.params.items():
                config[name] = param.sample()
        elif self.isethereal():
            lst = self.sample_ethereal()
            return lst
        else:
            config = self.sample_partial()

        return Transformer(self.name, self.path, config)

    def iscomplete(self):
        """Whether this Config Space is enough to sample an entire component
        (e.g. a subnode of MLP)."""
        return None not in [self.name, self.path]

    def isethereal(self):
        """Whether this Config Space is a result of CS operations like 'any',
        'seq' and 'shuffle' (and 'any'-like ones: 'rnd', 'ga', 'mtl', ...?)."""
        return None in [self.name, self.path] and len(self.params) > 0

    def sample_ethereal(self):
        """Sample from a node that is a result from a CS operation.

        Returns
        -------
        Nested lists of transformers.
        """
        lst = []

        # Fill list with transformers/lists from nested nodes.
        nested_node = self
        while nested_node.nested:
            nested_node = choice(nested_node.nested)
            lst.append(nested_node.sample())

        # Fill list with transformers/lists from child nodes.
        child_node = self
        while child_node.children:
            child_node = choice(child_node.children)
            lst.append(child_node.sample())

        return lst

    def sample_partial(self):
        """Sample from a node that is not a complete CS.

        Returns
        -------
        config
        """
        if self.nested:
            raise Exception('Partial CS cannot have nested CSs.')
        config = {}

        # Fill config with values from child nodes.
        child_node = choice(self.children)
        config.update(child_node.sample_partial())

        # Complete args with current node values, possibly overriding some
        # values from children/nested nodes (this happens with frozen cs())
        for name, param in self.params.items():
            config[name] = param.sample()

        return config

    def __str__(self, depth=''):
        rows = '\n'.join([f'  {k}: {v}' for k, v in self.params.items()])
        return f'{self.name}[\n{rows}\n]'

    __repr__ = __str__


class UnidentifiedConfigSpace(Exception):
    pass
