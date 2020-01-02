from pjml.config.parameter import FixedP


def freeze(cs, **kwargs):
    """Freeze args passed via kwargs

    Keyworded args are used to freeze some parameters of
    the algorithm, regardless of what a CS sampling could have chosen.
    TODO: it may be improved to effectively traverse and change the tree
    """
    # TODO: make real freeze inside the tree
    params = {} if cs.params is None else cs.params.copy()
    for k, v in kwargs.items():
        params[k] = FixedP(v)
    return cs.updated(params=params)
