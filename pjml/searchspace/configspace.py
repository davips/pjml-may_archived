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
        self.params = params
        self.nested = nested
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

        Sampling will return a tuple if it has children.
        """
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
        # some values from children/nested nodes (this happens with frozen cs())
        for name, param in self.params.items():
            try:
                config[name] = param.sample()
            except Exception as e:
                traceback.print_exc()
                print(e)
                print('Problems sampling: ', param.name, param)
                exit(0)

        if self.ispartial():
            return config
        elif self.isethereal():
            return []
        else:
            return Transformer(self.name, self.path, config)

    def iscomplete(self):
        """Whether this Config Space is enough to sample an entire component
        (e.g. a subnode of MLP)."""
        return None not in [self.name, self.path]

    def isethereal(self):
        """Whether this Config Space is a result of CS operations like 'any',
        'seq' and 'shuffle' (and 'any'-like ones: 'rnd', 'ga', 'mtl', ...?)."""
        return None in [self.name, self.path] and self.params is None

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
        rows = [str(self.params)]
        for child in self.children:
            rows.append(child.__str__(depth + '   '))
        return depth + self.__class__.__name__ + '\n'.join(rows) \
               + str(self.nested)

    __repr__ = __str__


class UnidentifiedConfigSpace(Exception):
    pass
