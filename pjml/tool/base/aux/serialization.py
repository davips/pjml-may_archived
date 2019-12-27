import json


def serialize(obj):
    return json.dumps(obj, sort_keys=True)


def deserialize(txt):
    return _dict_to_transformer(json.loads(txt))


def materialize(name, path, config):
    """Instantiate a transformer.

    Returns
    -------
    A ready to use component.
    """
    class_ = _get_class(path, name)
    return class_(**config)


def _dict_to_transformer(dic):
    """Convert recursively a dict to a transformer."""
    if 'transformer' not in dic:
        raise Exception('Provided dict does not represent a transformer.')
    name, path = dic['transf_id'].split('@')
    cfg = dic['config']
    if 'transformer' in cfg:
        cfg['transformer'] = _dict_to_transformer(cfg['transformer'])

    return materialize(name, path, cfg)


def _get_class(module, class_name):
    import importlib
    module = importlib.import_module(module)
    class_ = getattr(module, class_name)
    return class_
