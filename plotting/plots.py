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

def violinplot_smooth(ax, x, Y, tau, delta=.5, label=None, y_range=None, **kwargs):
    if type(x) != np.ndarray:
        x = np.atleast_1d(x)
    x = x.ravel()
    if type(Y) != np.ndarray:
        Y = np.atleast_2d(np.asarray(Y))
    if Y.shape[0] == 1:
        Y = Y.T
    if y_range is None:
        t = np.arange(np.amin(Y) - 3 * tau, np.amax(Y) + 3 * tau, tau / 10.)
    else:
        t = np.arange(y_range[0], y_range[1], tau / 10.)
    col = np.linspace(0, 1, len(t))
    c = np.r_[t, t[::-1]]
    cc = np.r_[col, col[::-1]]
    for j in xrange(Y.shape[1]):
        n = reduce(lambda a, b: a + b, [np.exp(-.5 * (t - yt) ** 2. / tau ** 2) for yt in Y[:, j]])
        n = n / np.amax(n) * delta
        y = x[j] + np.r_[n, -n[::-1]]

        ax.fill(y, c, label=label if j == 0 else None, **kwargs)
        ax.plot(y, c, '-k', lw=.5)

        ax.plot(0 * Y[:, j] + x[j], Y[:, j], 'ok', mfc='lightgray', markersize=2, lw=0)
