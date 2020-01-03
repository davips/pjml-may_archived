class NoAlgorithm(type):
    def __new__(cls, *args, **kwargs):
        raise Exception('NoAlgorithm is a singleton and shouldn\'t be instantiated')


class NoModel(type):
    def __new__(cls, *args, **kwargs):
        raise Exception('NoModel is a singleton and shouldn\'t be instantiated')
