import matplotlib.pyplot as plt
import matplotlib
import math


def plots(labels, plots_y, plot_x, xlabel, ylabel):
    if len(plots_y) != len(labels):
        return
    plt.figure(figsize=(20, 20))
    font = {'weight' : 'bold',
            'size' : 18}
    matplotlib.rc('font', **font)
    for i in range(len(plots_y)):
        plt.plot(plot_x, plots_y[i], label=labels[i])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.legend()
    plt.show()
