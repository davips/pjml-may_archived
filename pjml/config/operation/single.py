"""Operations over a single CS."""
from pjml.config.description.parameter import FixedP


def freeze(cs, **kwargs):
    """Freeze args passed via kwargs

    Keyworded args are used to freeze some parameters of
    the algorithm, regardless of what a CS sampling could have chosen.
    TODO: it may be improved to effectively traverse and change the tree
      in-place, not just extend overwritting it
    """
    params = {} if cs.params is None else cs.params.copy()
    for k, v in kwargs.items():
        params[k] = FixedP(v)
    return cs.updated(params=params)


def replace(cs, **kwargs):
    """Replace parameters in CS

    It can be used to replace a FixedP by a CatP, for instance.

    Example:
        File.cs  # contents:
        # ComponentCS(Node(
        #    params={
        #       'path': FixedP('./'),
        #       'name': FixedP('iris.arff')
        #   }
        # ))

        datasets = ['iris.arff', 'car.csv', 'abalone.arff']
        cs = replace(File.cs, name=CatP(choice, items=datasets))
        cs  # contents:
        # ComponentCS(Node(
        #    params={
        #       'path': FixedP('./'),
        #       'name': CatP(choice, items=datasets)
        #   }
        # ))


    TODO: it may be improved to effectively traverse and change the tree
        in-place, not just extend overwritting it
    """
    raise NotImplementedError
