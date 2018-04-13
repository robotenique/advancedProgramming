import numpy as np
import subprocess as sb
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def avg_graph(vsize):
    X = np.arange(0, 10)
    Y = np.zeros(X.shape)
    std_minus = np.zeros(X.shape)
    std_plus = np.zeros(X.shape)
    i = 0
    e = 1
    for n_if in range(0, 10):
        #np.linspace(0.01 , 0.04, 10)
        curr_data = np.array([])
        data = np.loadtxt(f'data_t20.txt', delimiter=',')
        curr_data = np.concatenate([curr_data, data[:, n_if]])
        print(curr_data)
        Y[n_if] = np.mean(curr_data)
        std_minus[n_if] = Y[n_if] - np.var(curr_data)
        std_plus[n_if] = Y[n_if] + np.var(curr_data)
    plt.xlabel('If number')
    plt.ylabel('Avg Time')
    plt.scatter(X[i:e], Y[i:e], s=100)
    plt.scatter(X[i:e], std_minus[i:e], s=50, facecolor="red", label=r"$\sqrt{\sigma}$")
    plt.scatter(X[i:e], std_plus[i:e], s=50, facecolor="red")
    plt.title(f"Fixed threads = 20, N = 5000000")
    plt.grid(True)
    plt.show()




def histogram(vsize):

    for n_if in range(0, 10):
        #np.linspace(0.01 , 0.04, 10)
        curr_data = np.array([])
        for v in vsize:
            data = np.loadtxt(f'data_t20.txt', delimiter=',')
            curr_data = np.concatenate([curr_data, data[:, n_if]])
        # the histogram of the data
        plt.hist(curr_data, alpha=0.5, label=f"{n_if} ifs", facecolor=np.random.rand(3,))
        print(f"Curr if = {n_if}, count = {curr_data.shape}")
    plt.xlabel('Time')
    plt.ylabel('Amount')
    plt.legend(loc='upper right')
    plt.title(f"Fixed threads = 20, N = 5000000")
    plt.grid(True)
    plt.show()


def get_runCommand(vector_size, num_threads):
    cmd = ['./contention.sh', str(vector_size), str(num_threads)]
    return cmd


def graph(v, threads_v):
    data = np.loadtxt(f'data_vv_{v}.txt', delimiter=',')*1e3
    #x = np.arange(data.shape[0]) + 1 # Threads actually start from 100
    x = threads_v
    y = np.arange(data.shape[1]) # Only 9 ifs
    X, Y = np.meshgrid(x, y)
    # f(X, Y) is actually data
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_title(f"Plot with array size = {v}")
    ax.contour3D(X, Y, data.T, 300, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_xlabel("Threads")
    ax.set_ylabel("Ifs")
    ax.set_zlabel("Time x1000")
    plt.show()




def main():
    vsize = (100, 1000, 10000, 100000)
    #avg_graph(vsize)
    numT =[1, 5, 10, 20, 30, 40, 45, 50,  100,  150,  200,  250,  300,  350,  400,  450,  500,
        550,  600,  650,  700,  750,  800,  850,  900,  950, 1000, 1050,
       1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600,
       1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150,
       2750, 2800, 2850, 2900, 2950, 3000, 3050, 3100, 3150, 3200, 3250,
       3300, 3350, 3400, 3450, 3500, 3550, 3600, 3650, 3700, 3750, 3800,
       3850, 3900, 3950, 4000, 4050, 4100, 4150, 4200, 4250, 4300, 4350,
       4400, 4450, 4500, 4550, 4600, 4650, 4700, 4750, 4800, 4850, 4900,
       4950]
    for v in vsize:
        graph(v, numT)


    # for v in vsize:
    #     with open(f"data_v{v}.txt", "w") as f:
    #         for t in numT:
    #             print(f"Running for {t} threads...")
    #             result = sb.check_output(get_runCommand(v, t)).decode("utf-8")
    #             f.writelines(result)
    # v = 5000
    # with open(f"data_t50000.txt", "w") as f:
    #     for _ in range(50):
    #         print(f"Running exp {_}...")
    #         result = sb.check_output(get_runCommand(v, 10000)).decode("utf-8")
    #         f.writelines(result)

if __name__ == '__main__':
    main()
