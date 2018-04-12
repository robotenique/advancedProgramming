import numpy as np
import subprocess as sb

def get_runCommand(vector_size, num_threads):
    cmd = ['./contention.sh', str(vector_size), str(num_threads)]
    return cmd


def main:
    vsize = np.arange(1, 10001, 100) - 1
    numT = np.arange(1, 5000, 50) - 1
    vsize[0] = 1
    numT[0] = 1

    for v, t in zip(vsize, numT):
