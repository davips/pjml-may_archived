from pjml.config.parameter import FixedP


def freeze(cs, **kwargs):
    """Freeze args passed via kwargs"""
    # TODO: make real freeze inside the tree
    params = {} if cs.params is None else cs.params.copy()
    for k, v in kwargs.items():
        params[k] = FixedP(v)
    return cs.updated(params=params)
