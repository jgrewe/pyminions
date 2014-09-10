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

def violinplot(ax, x, Y, tau, delta=.5, labels=None, y_range=None, **kwargs):
    """
    Produces a violinplot in the supplied axes.

    :param ax: Axes handle for the violin plot
    :param x:  x-positions of the violins
    :param Y: list of iterables with scalars points for the histograms (aka the y-values per x-value)
    :param tau: standard deviation of the smoothing Gaussian
    :param delta: half-width of violin
    :param labels: label for the single violins
    :param y_range: minimal and maximal y-values in a tuple
    :param **kwargs: keyword arguments passed to fill
    :return: list of smoothed histograms corresponding to each violin
    """
    if type(x) != np.ndarray:
        x = np.atleast_1d(x)
    x = x.ravel()

    if y_range is None:
        t = np.arange(np.amin(np.hstack(Y)) - 3 * tau, np.amax(np.hstack(Y)) + 3 * tau, tau / 10.)
    else:
        t = np.arange(y_range[0], y_range[1], tau / 10.)
    col = np.linspace(0, 1, len(t))
    c = np.r_[t, t[::-1]]
    cc = np.r_[col, col[::-1]]

    histograms = []

    if labels is None: labels = len(x)*[None]

    for (label, x,y) in zip(labels, x,Y):
        n = 0*t
        for yt in y:
            n[:] += np.exp(-.5 * (t - yt) ** 2. / tau ** 2)/np.sqrt(2*np.pi)/tau
        histograms.append(n)
        n = n / np.amax(n) * delta
        y2 = x + np.r_[n, -n[::-1]]

        ax.fill(y2, c, label=label, **kwargs)
        ax.plot(y2, c, '-k', lw=.5)
        ax.plot(0 * y + x, y, 'ok', mfc='lightgray', markersize=2, lw=0)
    return histograms