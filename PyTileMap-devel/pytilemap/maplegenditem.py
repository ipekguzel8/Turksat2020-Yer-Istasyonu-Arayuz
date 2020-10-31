from __future__ import print_function, absolute_import

from qtpy.QtCore import Qt, Slot, QRectF, QPointF
from qtpy.QtGui import QPen, QBrush, QColor
from qtpy.QtWidgets import QGraphicsObject, QGraphicsRectItem, QGraphicsItemGroup, \
    QGraphicsSimpleTextItem, QGraphicsEllipseItem, QGraphicsLineItem

from .mapitems import MapItem
from .functions import makePen, makeBrush
from .qtsupport import getQVariantValue


class MapLegendEntryItem(QGraphicsItemGroup):

    def __init__(self, shape, text, parent=None):
        QGraphicsItemGroup.__init__(self, parent=parent)

        text = QGraphicsSimpleTextItem(text, parent=shape)
        br = shape.boundingRect()
        x = br.right() + 10
        y = br.top() + 3
        text.setPos(x, y)
        self.addToGroup(shape)

        self._text = text

    def top(self):
        return self.boundingRect().top()

    def bottom(self):
        return self.boundingRect().bottom()

    def right(self):
        return self.boundingRect().right()

    def left(self):
        return self.boundingRect().left()

    def text(self):
        return self._text


class MapLegendItem(QGraphicsObject, MapItem):

    QtParentClass = QGraphicsObject

    def __init__(self, pos=None, parent=None):
        QGraphicsObject.__init__(self, parent=parent)
        MapItem.__init__(self)
        self.setZValue(200.0)

        self._anchorPos = QPointF(pos) if pos is not None else QPointF(10.0, 10.0)

        self._border = QGraphicsRectItem(parent=self)
        self._border.setPen(QPen(Qt.NoPen))
        self._border.setBrush(QBrush(QColor(190, 190, 190, 160)))

        self._entries = list()
        self._entriesGroup = QGraphicsItemGroup(parent=self)

    def _sceneChanged(self, oldScene, newScene):
        if oldScene is not None:
            oldScene.sceneRectChanged.disconnect(self.setSceneRect)
        if newScene is not None:
            newScene.sceneRectChanged.connect(self.setSceneRect)
            # Setup the new position of the item
            self.setSceneRect(newScene.sceneRect())

    def updatePosition(self, scene):
        pass

    def addPoint(self, text, color, border=None, size=20.0):
        shape = QGraphicsEllipseItem(size / 2.0, size / 2.0, size, size)
        brush = makeBrush(color)
        shape.setBrush(brush)
        shape.setPen(makePen(border))

        self.addEntry(MapLegendEntryItem(shape, text))

    def addRect(self, text, color, border=None, size=20.0):
        shape = QGraphicsRectItem(size / 2.0, size / 2.0, size, size)
        brush = makeBrush(color)
        shape.setBrush(brush)
        shape.setPen(makePen(border))

        self.addEntry(MapLegendEntryItem(shape, text))

    def addLine(self, text, color, width=1.):
        shape = QGraphicsLineItem(10., 10., 20., 20.)
        pen = makePen(color, width=width)
        shape.setPen(pen)
        self.addEntry(MapLegendEntryItem(shape, text))

    def addEntry(self, entry):
        self._entries.append(entry)
        self._entriesGroup.addToGroup(entry)
        self._updateLayout()

    def boundingRect(self):
        return self._border.boundingRect()

    def paint(*args, **kwargs):
        pass

    @Slot(QRectF)
    def setSceneRect(self, rect):
        self.setPos(rect.topLeft() + self._anchorPos)

    def _updateLayout(self):
        self.prepareGeometryChange()

        bottom = 0.0
        left = 0.0
        right = 0.0
        for entry in self._entries:
            entry.setPos(left, bottom)
            bottom += entry.bottom() + 5.0
            right = max(right, entry.right() + 5.0)

        self._border.setRect(0.0, 0.0, right, bottom + 5.0)

    def pen(self):
        """Pen for the background of the legend

        Returns:
            QPen: Pen for the background of the legend
        """
        return self._border.pen()

    def brush(self):
        """Brush for the background of the legend

        Returns:
            QBrush: Brush for the background of the legend
        """
        return self._border.brush()

    def setPen(self, *args, **kwargs):
        """Set the pen for the background of the legend

        The arguments are the same of the :func:`makePen` function
        """
        return self._border.setPen(makePen(*args, **kwargs))

    def setBrush(self, *args, **kwargs):
        """Set the brush for the background of the legend

        The arguments are the same of the :func:`makeBrush` function
        """
        return self._border.setBrush(makeBrush(*args, **kwargs))

