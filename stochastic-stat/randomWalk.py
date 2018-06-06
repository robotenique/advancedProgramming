"""Simualates a very simple random walk (1-D), with probability = 1/2
"""

import matplotlib.pyplot as plt
import numpy as np
import random as r

def main():
    experiments = 3
    max_num = 500
    global_data = []
    for _ in range(experiments):
        axis_y = [0]
        for i in range(max_num):
            axis_y.append(1 if r.random() > 0.5 else -1)
        global_data.append(axis_y)

    plot_graph(gen_s, global_data, max_num=max_num, title=r"Sequência $S_n$")
    plot_graph(gen_y, global_data, max_num=max_num, title=r"Sequência $Y_n$")
    plot_graph(gen_z, global_data, max_num=max_num, title=r"Sequência $Z_n$")

def gen_s(global_data):
    for seq in global_data:
        axis_y = [0]
        for i in range(1, len(seq)):
            axis_y.append(axis_y[i - 1] + seq[i])
        yield axis_y

def gen_y(global_data):
    for seq in global_data:
        axis_y = [0]
        for i in range(1, len(seq)):
            axis_y.append(sum(seq[1:i + 1])/i)
        yield axis_y

def gen_z(global_data):
    for seq in global_data:
        axis_y = [0, seq[1]]
        last_exp = seq[1]
        for i in range(2, len(seq)):
            axis_y.append((last_exp + seq[i])/2)
            last_exp = seq[i]
        yield axis_y

def plot_graph(generate_axis, global_data, max_num=500, title=""):
    plt.figure(figsize=(10, 6))
    axis_x = np.arange(0, max_num + 1, 1)
    for style, axis_y in zip(("-", "--", ":"), generate_axis(global_data)):
        plt.plot(axis_x, axis_y, style, linewidth=2.5)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(title+".png")


if __name__ == '__main__':
    main()
