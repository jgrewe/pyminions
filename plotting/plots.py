__author__ = 'Fabian Sinz'
from matplotlib import cm
from matplotlib.patches import Rectangle
import numpy as np

def hinton(ax, mu, sigma, mu_max=None, sigma_max=None, cmap=None):
    """
    Plots a Hinton plot into the axis. The means are depicted as
    square size while the standard deviations are depicted by color.

    :param ax: matplotlib axis handle
    :param mu: two dimensional numpy array
    :param sigma: two dimensional numpy array
    :param mu_max: scalar for manually setting the maximal value of mu
    :param sigma_max: scalar for manually setting the maximal value of sigma
    :param cmap: colormap
    :return: the result of add_patch (e.g. to use for a colorbar)
    """
    if cmap is None:
        cmap = cm.jet

    if mu_max is None:  mu_max = np.amax(np.abs(mu))
    if sigma_max is None:  sigma_max = np.amax(np.abs(sigma))

    ax.patch.set_facecolor([0, 0, 0, 0])

    for (x, y), w in np.ndenumerate(mu):
        s = sigma[x, y]
        color = cmap(s / sigma_max)
        size = np.abs(w / mu_max)
        rect = Rectangle([x - size / 2, y - size / 2], size, size,
                         facecolor=color, edgecolor=color)
        ret = ax.add_patch(rect)
    ax.axis('tight')
    try:
        ax.set_aspect('equal', 'box')
    except:
        pass
    ax.autoscale_view()
    ax.invert_yaxis()
    return ret
