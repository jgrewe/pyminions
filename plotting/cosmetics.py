from itertools import cycle
import string
from IPython import embed
__author__ = 'Fabian Sinz, Jan Grewe'


def box_off(ax, where=None):
    """
    Removes axes form an matplotlib axis handle. The variable where
    specifies which axes are to be removed.

    :param ax: matplotlib axis handle
    :param where: list with one or more of the following elements: 'left', 'right', 'bottom', 'top' (default: ['right', 'top'])
    """
    if where is None: where = ['right', 'top']
    for loc, spine in ax.spines.iteritems():
        if loc in where:
            spine.set_color('none')  # don't draw spine
        else:
            continue
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')


def label_axes(fig, labels=None, loc=None, **kwargs):
    """
    Walks through axes and labels each.

    kwargs are collected and passed to `annotate`

    From (http://stackoverflow.com/questions/22508590/enumerate-plots-in-matplotlib-figure)
    under creative commons license (http://creativecommons.org/licenses/by-sa/3.0/).

    :param fig: Figure object to work on
    :type fig: matplotlib.figure.Figure
    :param labels: iterable of strings to use to label the axes. If None, lower case letters are used.
    :type labels: iterable or None
    :param loc: Where to put the label in axes-fraction units
    :type loc: len=2 tuple of floats

    """
    if labels is None:
        labels = string.lowercase

    # re-use labels rather than stop labeling
    labels = cycle(labels)
    if loc is None:
        loc = (.9, .9)
    for ax, lab in zip(fig.axes, labels):
        ax.annotate(lab, xy=loc,
                    xycoords='axes fraction',
                    **kwargs)


def set_boxplot_colors(boxplot, colors):
    """

        Changes the color of boxplot boxes, whiskers, medians and caps.

    @param boxplot: the boxplot @type dict
    @param colors: list of colors that @type list

    """
    if not ("boxes" in boxplot.keys() and "medians" in boxplot.keys() and
            "caps" in boxplot.keys() and "whiskers" in boxplot.keys()):
        raise ValueError("Argument passed as boxplot arg, does not describe a boxplot!")

    if len(colors) is not len(boxplot['boxes']):
        print("Error! I need an extra color for each boxplot! Provided %i colors for %i boxes!" % len(colors), len(boxplot['boxes']))
        return
    for box, med, color in zip(boxplot['boxes'], boxplot['medians'], colors):
        box.set_color(color)
        med.set_color(color)

    for i, z in enumerate(zip(boxplot['whiskers'], boxplot['caps'])):
        whisker, cap = z
        whisker.set_color(colors[i / 2])
        cap.set_color(colors[i / 2])
