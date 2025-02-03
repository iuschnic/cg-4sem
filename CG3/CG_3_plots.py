import matplotlib.pyplot as plt
import matplotlib
import math


def plots_by_angles(fir, sec, thrd, frth, fifth, labels, head, y_label, option):
    if not fir or not sec or not thrd or not frth:
        return -1
    font = {'weight' : 'bold',
            'size' : 18}
    matplotlib.rc('font', **font)
    fig, ax = plt.subplots(2, 3, figsize=(30, 20))
    fig.suptitle(head)
    fig.delaxes(ax[1][2])

    data = []
    angles = []
    for elem in fir:
        data.append(elem[0])
        angles.append(elem[1])
    if option == 0:
        ax[0][0].plot(angles, data)
    else:
        ax[0][0].bar(angles, data)
    ax[0][0].set_title(labels[0])
    ax[0][0].set_xlabel("Угол, градусы")
    ax[0][0].set_ylabel(y_label)

    data = []
    angles = []
    for elem in sec:
        data.append(elem[0])
        angles.append(elem[1])
    if option == 0:
        ax[0][1].plot(angles, data)
    else:
        ax[0][1].bar(angles, data)
    ax[0][1].set_title(labels[1])
    ax[0][1].set_xlabel("Угол, градусы")
    ax[0][1].set_ylabel(y_label)

    data = []
    angles = []
    for elem in thrd:
        data.append(elem[0])
        angles.append(elem[1])
    if option == 0:
        ax[1][0].plot(angles, data)
    else:
        ax[1][0].bar(angles, data)
    ax[1][0].set_title(labels[2])
    ax[1][0].set_xlabel("Угол, градусы")
    ax[1][0].set_ylabel(y_label)

    data = []
    angles = []
    for elem in frth:
        data.append(elem[0])
        angles.append(elem[1])
    if option == 0:
        ax[1][1].plot(angles, data)
    else:
        ax[1][1].bar(angles, data)
    ax[1][1].set_title(labels[3])
    ax[1][1].set_xlabel("Угол, градусы")
    ax[1][1].set_ylabel(y_label)

    data = []
    angles = []
    for elem in fifth:
        data.append(elem[0])
        angles.append(elem[1])
    if option == 0:
        ax[0][2].plot(angles, data)
    else:
        ax[0][2].bar(angles, data)
    ax[0][2].set_title(labels[4])
    ax[0][2].set_xlabel("Угол, градусы")
    ax[0][2].set_ylabel(y_label)

    plt.show()


def plots_average(groups, data):
    font = {'weight': 'bold',
            'size': 18}
    matplotlib.rc('font', **font)
    plt.figure(figsize=(30, 20))
    plt.bar(groups, data)
    plt.ylabel("Среднее время, нс")
    plt.show()
