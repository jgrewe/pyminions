__author__ = 'Fabian Sinz'


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
            raise ValueError('unknown spine location: %s' % loc)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')