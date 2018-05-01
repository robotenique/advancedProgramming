import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import scipy.stats as st
from sys import argv

def main():
    print("Algorithm  | Time (ns) | Average (of accesses) | Std (of accesses) | Times each thread entered the critical section")
    if len(argv) < 2:
        filename = "result_10_5000000_RR.txt"
    else:
        filename = argv[1]
    data = np.loadtxt(filename, delimiter=',')
    alg_bakery = []
    alg_gate = []

    for d in data:
        new = AlgorithmTest(d)
        if new.alg == 1:
            alg_bakery.append(new)
        else:
            alg_gate.append(new)

    thread_access_plot(alg_bakery)
    thread_access_plot(alg_gate)


def thread_access_plot(alg_tests):
    num_threads = alg_tests[0].threads
    accesses = []
    times = []
    for alg_t in alg_tests:
        accesses.append(alg_t.accesses)
        times.append(alg_t.time)
    times = np.array(times)*1e-3
    print(np.std(times))
    times = get_CI(times)
    accesses = np.array(accesses)
    stds = np.sqrt(np.std(accesses, axis=0))
    accesses = np.sum(accesses, axis=0)*1/len(alg_tests)
    std_mean = np.std(accesses)

    print(f"Standard Deviation: {std_mean}, mean ={np.mean(accesses)}, Time conf interval (95%) = {times}")
    fig, ax = plt.subplots()
    index = np.arange(num_threads) + 1
    bar_width = 0.8
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = ax.bar(index, accesses, bar_width,
                    alpha=opacity, color=np.random.rand(3, ),
                    error_kw=error_config,
                    label='Threads')

    ax.set_xlabel('Thread')
    ax.set_ylabel('Accesses to the Critical Section')
    ax.set_title(f"Algorithm : {alg_tests[0].alg_str()}")
    ax.set_xticks((index - bar_width/6))
    if num_threads < 20:
        ax.set_xticklabels((str(i+1) for i in range(num_threads)))
    else:
        ax.set_xticklabels("")
    ax.legend()

    plt.show()

def get_CI(v, opt=False):
    # If opt == true, returns the 't' value, not the [avg - t, avg + t]
    if opt:
        ci = st.t.interval(0.95, len(v) - 1, loc=np.mean(v), scale=st.sem(v))
        arr = [0, 0]
        arr[0] = np.mean(v) - ci[0]
        arr[1] =ci[1] - np.mean(v)
        return arr #[t, t]
    return st.t.interval(0.95, len(v) - 1, loc=np.mean(v), scale=st.sem(v))

class AlgorithmTest(object):
    def __init__(self, experiment, filename=""):
        e = experiment
        self.alg = int(e[0])
        self.filename = filename
        self.time = e[1]
        self.avg = e[2]
        self.std = e[3]
        self.accesses = e[4:].astype(int)
        self.threads = len(self.accesses)

    def alg_str(self):
        t = "Bakery" if self.alg == 1 else "Gate"
        return t+" | "+self.filename

    def __str__(self):
        t = "Bakery" if self.alg == 1 else "Gate"
        return f"[{t}]: time = {self.time} ns , avg = {self.avg} , std = {self.std} , num threads = {self.threads}, accesses = {self.accesses}"

    def __repr__(self):
        t = "Bakery" if self.alg == 1 else "Gate"
        return f"[{t}]: time = {self.time} ns , avg = {self.avg} , std = {self.std} , num threads = {self.threads}, accesses = {self.accesses}"

if __name__ == '__main__':
    main()
