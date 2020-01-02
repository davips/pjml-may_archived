from numpy.random import randint


def choice(items):
    if len(items) == 0:
        raise Exception('No choice from Empty list!')
    idx = randint(0, len(items))
    return items[idx]
