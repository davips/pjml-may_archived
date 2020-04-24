from functools import partial

from time import sleep

from cururu.worker import Worker, Nothing
from pjml.tool.abc.mixin.timers import Timers


def f(a, b):
    print('start', a, b)
    sleep(a + b)
    print('end', a, b)
    print()
    return Nothing


start = Timers._clock()

w = Worker()
w.put((f, {'a': 2, 'b': 1}))
w.put((f, {'a': 0, 'b': 1}))
w.put((f, {'a': 2, 'b': 0}))

print('Tempo: ', '{:.2f}'.format(Timers._clock() - start))
w.join()
print('Tempo tot: ', Timers._clock() - start)
