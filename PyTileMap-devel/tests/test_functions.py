import pytest
import numpy as np

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QBrush, QPen


from pytilemap.functions import makeColorFromInts, makeColorFromFloats, makeColorFromStr, \
    makeColorFromList, makeColorFromNdArray, makeColor, makeBrush, makePen, clip

SolidLine = Qt.SolidLine
DashLine = Qt.DashLine
SolidPattern = Qt.SolidPattern
NoBrush = Qt.NoBrush
Dense1Pattern = Qt.Dense1Pattern


COLOR_ARG_LIST_INT = [(1, 2, 3), (1, 2, 3, 4), [1, 2, 3]]
COLOR_ARG_LIST_INT_REF = [QColor(1, 2, 3), QColor(1, 2, 3, 4), QColor(1, 2, 3)]

COLOR_ARG_LIST_FLOAT = [(0.1, 0.2, 0.3), (0.1, 0.2, 0.3, 0.4), [0.1, 0.2, 0.3]]
COLOR_ARG_LIST_FLOAT_REF = [QColor(0.1 * 255, 0.2 * 255, 0.3 * 255),
                            QColor(0.1 * 255, 0.2 * 255, 0.3 * 255, 0.4 * 255),
                            QColor(0.1 * 255, 0.2 * 255, 0.3 * 255)]

COLOR_ARG_LIST_STR = ['#FFAA11', 'green']
COLOR_ARG_LIST_STR_REF = [QColor(255, 170, 17), QColor(0, 128, 0)]

COLOR_ARG_NDARRAY_INT3 = np.asarray([[1, 2, 3], [4, 5, 6]], dtype=np.int64)
COLOR_ARG_NDARRAY_INT3_REF = [QColor(1, 2, 3), QColor(4, 5, 6)]
COLOR_ARG_NDARRAY_INT4 = np.asarray([[1, 2, 3, 4], [4, 5, 6, 7]], dtype=np.int64)
COLOR_ARG_NDARRAY_INT4_REF = [QColor(1, 2, 3, 4), QColor(4, 5, 6, 7)]

COLOR_ARG_NDARRAY_FLOAT3 = np.asarray([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]], dtype=np.float64)
COLOR_ARG_NDARRAY_FLOAT3_REF = [QColor(0.1 * 255, 0.2 * 255, 0.3 * 255),
                                QColor(0.4 * 255, 0.5 * 255, 0.6 * 255)]
COLOR_ARG_NDARRAY_FLOAT4 = np.asarray([[0.1, 0.2, 0.3, 0.4], [0.4, 0.5, 0.6, 0.7]], dtype=np.float64)
COLOR_ARG_NDARRAY_FLOAT4_REF = [QColor(0.1 * 255, 0.2 * 255, 0.3 * 255, 0.4 * 255),
                                QColor(0.4 * 255, 0.5 * 255, 0.6 * 255, 0.7 * 255)]


@pytest.mark.parametrize('colorArgs,qcolor', [
    ((1, 2, 3, 4), QColor(1, 2, 3, 4)),
    ((1, 2, 3), QColor(1, 2, 3, 255)),
    ((1, 2, 3), QColor(1, 2, 3)),
])
def test_color_from_ints(colorArgs, qcolor):
    color = makeColorFromInts(colorArgs)
    assert color == qcolor


@pytest.mark.parametrize('colorArgs,qcolor', [
    ((0.1, 0.2, 0.3, 0.4), QColor(0.1 * 255, 0.2 * 255, 0.3 * 255, 0.4 * 255)),
    ((0.1, 0.2, 0.3), QColor(0.1 * 255, 0.2 * 255, 0.3 * 255, 255)),
    ((0.1, 0.2, 0.3), QColor(0.1 * 255, 0.2 * 255, 0.3 * 255)),
])
def test_color_from_floats(colorArgs, qcolor):
    color = makeColorFromFloats(colorArgs)
    assert color == qcolor


@pytest.mark.parametrize('colorArgs,qcolor', [
    ('#FFAA11', QColor(255, 170, 17)),
    ('green', QColor(0, 128, 0)),
])
def test_color_from_strings(colorArgs, qcolor):
    color = makeColorFromStr(colorArgs)
    assert color == qcolor


@pytest.mark.parametrize('colorArgs,qcolor', [
    (COLOR_ARG_LIST_INT, COLOR_ARG_LIST_INT_REF),
    (COLOR_ARG_LIST_FLOAT, COLOR_ARG_LIST_FLOAT_REF),
    (COLOR_ARG_NDARRAY_INT3, COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT3.astype(np.int32), COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT4, COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_INT4.astype(np.int32), COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT3, COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT3.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT4, COLOR_ARG_NDARRAY_FLOAT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT4.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT4_REF),
])
def test_color_from_list(colorArgs, qcolor):
    color = makeColorFromList(colorArgs)
    assert color == qcolor


@pytest.mark.parametrize('colorArgs,qcolor', [
    (COLOR_ARG_NDARRAY_INT3, COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT3.astype(np.int32), COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT4, COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_INT4.astype(np.int32), COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT3, COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT3.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT4, COLOR_ARG_NDARRAY_FLOAT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT4.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT4_REF),
])
def test_color_from_ndarray(colorArgs, qcolor):
    color = makeColorFromNdArray(colorArgs)
    assert color == qcolor


@pytest.mark.parametrize('colorArgs,qcolor', [
    ((1, 2, 3, 4), QColor(1, 2, 3, 4)),
    ((1, 2, 3), QColor(1, 2, 3, 255)),
    ((0.1, 0.2, 0.3, 0.4), QColor(0.1 * 255, 0.2 * 255, 0.3 * 255, 0.4 * 255)),
    ((0.1, 0.2, 0.3), QColor(0.1 * 255, 0.2 * 255, 0.3 * 255, 255)),
    ('#FFAA11', QColor(255, 170, 17)),
    ('green', QColor(0, 128, 0)),
    (COLOR_ARG_LIST_INT, COLOR_ARG_LIST_INT_REF),
    (COLOR_ARG_LIST_FLOAT, COLOR_ARG_LIST_FLOAT_REF),
    (COLOR_ARG_NDARRAY_INT3, COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT3.astype(np.int32), COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT4, COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_INT4.astype(np.int32), COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT3, COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT3.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT4, COLOR_ARG_NDARRAY_FLOAT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT4.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT4_REF),
])
def test_color_default(colorArgs, qcolor):
    color = makeColor(colorArgs)
    assert color == qcolor


@pytest.mark.parametrize('colorArgs,qcolor', [
    ((1, 2, 3, 4), QColor(1, 2, 3, 4)),
    ((1, 2, 3), QColor(1, 2, 3, 255)),
    ((0.1, 0.2, 0.3, 0.4), QColor(0.1 * 255, 0.2 * 255, 0.3 * 255, 0.4 * 255)),
    ((0.1, 0.2, 0.3), QColor(0.1 * 255, 0.2 * 255, 0.3 * 255, 255)),
    ('#FFAA11', QColor(255, 170, 17)),
    ('green', QColor(0, 128, 0)),
])
@pytest.mark.parametrize('style', [SolidPattern, NoBrush, Dense1Pattern])
def test_make_brush_single_color(colorArgs, qcolor, style):
    testBrush = makeBrush(colorArgs, style=style)
    assert testBrush == QBrush(qcolor, style=style)


@pytest.mark.parametrize('colorArgs,qcolor', [
    (COLOR_ARG_LIST_INT, COLOR_ARG_LIST_INT_REF),
    (COLOR_ARG_LIST_FLOAT, COLOR_ARG_LIST_FLOAT_REF),
    (COLOR_ARG_NDARRAY_INT3, COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT3.astype(np.int32), COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT4, COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_INT4.astype(np.int32), COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT3, COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT3.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT4, COLOR_ARG_NDARRAY_FLOAT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT4.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT4_REF),
])
@pytest.mark.parametrize('style', [SolidPattern, NoBrush, Dense1Pattern])
def test_make_brush_list_of_colors(colorArgs, qcolor, style):
    testBrush = makeBrush(colorArgs, style=style)
    refBrushes = [QBrush(c, style=style) for c in qcolor]
    assert testBrush == refBrushes


@pytest.mark.parametrize('colorArgs,qcolor', [
    ((1, 2, 3, 4), QColor(1, 2, 3, 4)),
    ((1, 2, 3), QColor(1, 2, 3, 255)),
    ((0.1, 0.2, 0.3, 0.4), QColor(0.1 * 255, 0.2 * 255, 0.3 * 255, 0.4 * 255)),
    ((0.1, 0.2, 0.3), QColor(0.1 * 255, 0.2 * 255, 0.3 * 255, 255)),
    ('#FFAA11', QColor(255, 170, 17)),
    ('green', QColor(0, 128, 0)),
])
@pytest.mark.parametrize('style', [SolidLine, DashLine])
@pytest.mark.parametrize('width', [0.0, 1, 3.])
def test_make_pen_single_color(colorArgs, qcolor, width, style):
    testPen = makePen(colorArgs, width=width, style=style)
    assert testPen == QPen(QBrush(qcolor), width, style=style)


@pytest.mark.parametrize('colorArgs,qcolor', [
    (COLOR_ARG_LIST_INT, COLOR_ARG_LIST_INT_REF),
    (COLOR_ARG_LIST_FLOAT, COLOR_ARG_LIST_FLOAT_REF),
    (COLOR_ARG_NDARRAY_INT3, COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT3.astype(np.int32), COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT4, COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_INT4.astype(np.int32), COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT3, COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT3.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT4, COLOR_ARG_NDARRAY_FLOAT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT4.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT4_REF),
])
@pytest.mark.parametrize('style', [SolidLine, DashLine])
@pytest.mark.parametrize('width', [0., 1, 3.])
def test_make_pen_list_of_colors(colorArgs, qcolor, width, style):
    testPen = makePen(colorArgs, width=width, style=style)
    refPen = [QPen(QBrush(c), width, style=style) for c in qcolor]
    assert testPen == refPen


@pytest.mark.parametrize('colorArgs,qcolor', [
    (COLOR_ARG_LIST_INT, COLOR_ARG_LIST_INT_REF),
    (COLOR_ARG_LIST_FLOAT, COLOR_ARG_LIST_FLOAT_REF),
    (COLOR_ARG_NDARRAY_INT3, COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT3.astype(np.int32), COLOR_ARG_NDARRAY_INT3_REF),
    (COLOR_ARG_NDARRAY_INT4, COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_INT4.astype(np.int32), COLOR_ARG_NDARRAY_INT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT3, COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT3.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT3_REF),
    (COLOR_ARG_NDARRAY_FLOAT4, COLOR_ARG_NDARRAY_FLOAT4_REF),
    (COLOR_ARG_NDARRAY_FLOAT4.astype(np.float32), COLOR_ARG_NDARRAY_FLOAT4_REF),
])
@pytest.mark.parametrize('style', [SolidLine, DashLine])
@pytest.mark.parametrize('width', [(0., 1, 3.)])
def test_make_pen_list_of_colors_and_widths(colorArgs, qcolor, width, style):
    testPen = makePen(colorArgs, width=width, style=style)
    refPen = [QPen(QBrush(c), w, style=style) for c, w in zip(qcolor, width)]
    assert testPen == refPen


@pytest.mark.parametrize('value,minValue,maxValue,expectedResult', [
    (1, 0, 3, 1), (1., 0., 3., 1.),
    (1, 2, 3, 2), (1., 2., 3., 2.),
    (1, -2, 0, 0), (1., -2., 0., 0.),
])
def test_clip(value, minValue, maxValue, expectedResult):

    testResult = clip(value, minValue, maxValue)
    assert testResult == expectedResult
