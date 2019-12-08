class ConfigSpace:
    def __init__(self, name=None, path=None, params=None, nested=None, children=None):
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

    # def sample(self):
    #     """TODO:
    #     """
    #     if None in [self.name, self.path]:
    #           raise UnidentifiedConfigSpace()
    #     config = self._elem_hps_to_config(self)
    #
    #     return config
    #
    # def _elem_hps_to_config(self, node):
    #     args = {}
    #
    #     for name, hp in node.hps.items():
    #         try:
    #             args[name] = hp.sample()
    #         except Exception as e:
    #             traceback.print_exc()
    #             print(e)
    #             print('Problems sampling: ', hp.name, hp)
    #             exit(0)
    #
    #     if node.children:
    #         child = choice(node.children)
    #
    #         config = self._elem_hps_to_config(child)
    #         args.update(config)  # freeze: hps filhos se sobrepõe ao hps atual!
    #
    #     return args
    #
    # def __str__(self, depth=''):
    #     rows = [str(self.params)]
    #     for child in self.children:
    #         rows.append(child.__str__(depth + '   '))
    #     return depth + self.__class__.__name__ + '\n'.join(rows) \
    #            + str(self.nested)
    #
    # __repr__ = __str__
