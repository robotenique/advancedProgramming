import numpy as np
import subprocess as sb
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def histogram(vsize):

    for n_if in range(0, 10):
        curr_data = np.array([])
        for v in vsize:
            data = np.loadtxt(f'data_t3000.txt', delimiter=',')
            curr_data = np.concatenate([curr_data, data[:, n_if]])
        # the histogram of the data
        plt.hist(curr_data, alpha=0.5, label=f"{n_if} ifs", facecolor=np.random.rand(3,))
        print(f"Curr if = {n_if}, count = {curr_data.shape}")
    plt.xlabel('Time')
    plt.ylabel('Amount')
    plt.legend(loc='upper right')
    plt.title(f"Fixed threads = 3000, N = 10000")
    plt.grid(True)
    plt.show()


def get_runCommand(vector_size, num_threads):
    cmd = ['./contention.sh', str(vector_size), str(num_threads)]
    return cmd


def graph(v):
    data = np.loadtxt(f'data_v{v}.txt', delimiter=',')*1e3
    #x = np.arange(data.shape[0]) + 1 # Threads actually start from 100
    x = np.arange(1, 5000, 50) - 1
    x[0] = 1 # The first number can't be zero
    y = np.arange(data.shape[1]) # Only 9 ifs
    X, Y = np.meshgrid(x, y)
    # f(X, Y) is actually data
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_title(f"Plot with array size = {v}")
    ax.contour3D(X, Y, data.T, 200, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_xlabel("Threads")
    ax.set_ylabel("Ifs")
    ax.set_zlabel("Time x1000")
    plt.show()




def main():
    #vsize = (100, 1000, 10000, 100000)
    #histogram(vsize)
    # for v in vsize:
    #     graph(v)
    # numT = np.arange(1, 5000, 50) - 1
    # numT[0] = 1 # The first number can't be zero
    # for v in vsize:
    #     with open(f"data_v{v}.txt", "w") as f:
    #         for t in numT:
    #             print(f"Running for {t} threads...")
    #             result = sb.check_output(get_runCommand(v, t)).decode("utf-8")
    #             f.writelines(result)
    v = 5000
    with open(f"data_t50000.txt", "w") as f:
        for _ in range(50):
            print(f"Running exp {_}...")
            result = sb.check_output(get_runCommand(v, 10000)).decode("utf-8")
            f.writelines(result)
if __name__ == '__main__':
    main()
