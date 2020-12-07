import numpy as np
from matplotlib import pyplot as plt
from matplotlib import collections  as mc

n_solutions = 0

def visualize(lines, widths):
    widths = 10 * np.array(widths)

    lc = mc.LineCollection(lines, linewidths=widths, zorder=1)

    fig, ax = plt.subplots()
    ax.add_collection(lc)
    xs = []
    ys = []
    for a, b in lines:
        xs.append(a[0])
        ys.append(a[1])
        xs.append(b[0])
        ys.append(b[1])

    ax.scatter(xs, ys, s=60, c='red', zorder=2)
    ax.autoscale()
    global n_solutions
    ax.margins(0.1)
    fig.savefig('solution_' + str(n_solutions) + '.png', bbox_inches='tight')
    n_solutions += 1
    plt.close(fig)
