"""
text book checker debug file
@author: tang142857
Copyright(c) DFSA Software Develop Center
"""
from time import time


def timer(fun):
    def reFunction(*args, **kwargs):
        startTime = time()
        print('Running...')
        fun(*args, **kwargs)
        print(f'Down used {time()-startTime}seconds')

    return reFunction