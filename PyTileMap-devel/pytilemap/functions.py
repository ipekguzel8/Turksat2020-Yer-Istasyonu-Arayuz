import sys
import sip
import numpy as np

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QBrush, QPen

SolidLine = Qt.SolidLine
SolidPattern = Qt.SolidPattern
SquareCap = Qt.SquareCap
BevelJoin = Qt.BevelJoin


__all__ = [
    'iterRange',
    'makeColorFromInts',
    'makeColorFromFloats',
    'makeColorFromStr',
    'makeColorFromNdArray',
    'makeColorFromList',
    'makeColor',
    'makeBrush',
    'makePen',
    'clip',
]

PYTHON_VERSION = sys.version_info[0]

if PYTHON_VERSION == 2:
    iterRange = xrange
    import itertools
    izip = itertools.izip
else:
    iterRange = range
    izip = zip


def makeColorFromInts(ints):
    """Create a color from list or tuple of integers

    Args:
        ints (tuple[int]): Integers [0, 255] values for the color. May be 3 or 4 for the alpha color.

    Retuns:
        QColor: color
    """
    r = ints[0]
    g = ints[1]
    b = ints[2]
    a = ints[3] if len(ints) == 4 else 255
    return QColor(r, g, b, a)


def makeColorFromFloats(floats):
    """Create a color from list or tuple of floats

    Args:
        floats (tuple[float]): Float [0.0, 1.0] values for the color. May be 3 or 4 for the alpha color.

    Retuns:
        QColor: color
    """
    r = int(floats[0] * 255.0)
    g = int(floats[1] * 255.0)
    b = int(floats[2] * 255.0)
    a = int(floats[3] * 255.0) if len(floats) == 4 else 255
    return QColor(r, g, b, a)


def makeColorFromStr(name):
    """Create a color from a string

    Args:
        name (str): name or html string of the color

    Retuns:
        QColor: color
    """
    return QColor(name)


def makeColorFromNdArray(array):
    """Create a list of colors from a numpy array

    Args:
        array (numpy.ndarray): (Nx3) or (Nx4) numpy array with number in range [0, 255] or [0.0, 1.0]

    Retuns:
        list[QColor]: List of colors
    """
    if array.dtype in [np.float32, np.float64]:
        array = np.asarray(array * 255.0, dtype=np.int32)

    return [makeColorFromInts(row) for row in array]


def makeColorFromList(colorList):
    """Create a list of colors from a list, tuple or numpy array

    Args:
        colorList (list,tuplenumpy.ndarray): List, tuple or numpy array. The elements must have length of 3 or 4
            and the numbers must be in range [0, 255] or [0.0, 1.0]

    Retuns:
        list[QColor]: List of colors
    """
    colors = list()
    if len(colorList) == 0:
        return colors

    element = colorList[0][0]
    if isinstance(element, (float, np.floating)):
        makeFunction = makeColorFromFloats
    elif isinstance(element, (int, np.integer)):
        makeFunction = makeColorFromInts
    elif isinstance(element, str):
        makeFunction = makeColorFromStr
    else:
        makeFunction = QColor

    return [makeFunction(row) for row in colorList]


def makeColor(args):
    """Convenience function for creating a QColor or a list of QColors.

    Args:
        args: Argument for creating QColor[s]

    Return:
        list[QColor],QColor: Created QColor[s].

    See:
        :func:`makeColorFromInts`
        :func:`makeColorFromFloats`
        :func:`makeColorFromStr`
        :func:`makeColorFromNdArray`
        :func:`makeColorFromList`
    """
    makeFunction = QColor
    if isinstance(args, str):
        makeFunction = makeColorFromStr
    elif isinstance(args, tuple):
        if isinstance(args[0], int):
            makeFunction = makeColorFromInts
        else:
            makeFunction = makeColorFromFloats
    elif isinstance(args, np.ndarray):
        makeFunction = makeColorFromNdArray
    elif isinstance(args, list):
        makeFunction = makeColorFromList

    return makeFunction(args)


def makeBrush(color, style=SolidPattern):
    if color is None:
        return QBrush(Qt.NoBrush)
    if isinstance(color, QBrush):
        return QBrush(color)
    color = makeColor(color)
    if isinstance(color, list):
        return [QBrush(c, style) for c in color]
    return QBrush(color, style)


def makePen(color, width=1.0, style=SolidLine, cap=SquareCap, join=BevelJoin):
    if color is None:
        return QPen(Qt.NoPen)
    if isinstance(color, QPen):
        return QPen(color)
    brush = makeBrush(color)
    if isinstance(brush, list):
        if not hasattr(width, '__iter__'):
            width = np.full(len(brush), width, dtype=np.float64)
        return [QPen(b, w, style=style) for b, w in izip(brush, width)]
    return QPen(brush, width, style=style, cap=cap, join=join)


def clip(value, minValue, maxValue):
    return min(maxValue, max(minValue, value))
