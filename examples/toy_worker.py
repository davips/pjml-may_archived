from functools import partial

from time import sleep

from cururu.worker import Worker
from pjml.tool.abc.mixin.timers import Timers


def f(a, b):
    print('start', a, b)
    sleep(a + b)
    print('end', a, b)
    print()


start = Timers._clock()

w = Worker(parallel= False)
w.put(partial(f, 2, 1))
w.put(partial(f, 0, 1))
w.put(partial(f, 2, 0))

print('Tempo: ', '{:.2f}'.format(Timers._clock() - start))
w.join()
print('Tempo tot: ', Timers._clock() - start)
