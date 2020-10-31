import numpy as np

from qtpy.QtCore import Qt, Slot, QPointF, QRectF
from qtpy.QtGui import QFontMetrics, QFont
from qtpy.QtWidgets import QGraphicsObject


from .mapitems import MapItem
from .functions import makePen, makeBrush, clip
from .qtsupport import getQVariantValue


class MapScaleItem(QGraphicsObject, MapItem):
    """Scale bar for the visualization of the scale of teh map.

    The scale bar is located on the bottom right of the map and can' be moved.
    The scale bar accepts hover events and change its color.
    """

    QtParentClass = QGraphicsObject

    EarthCircumference = 1000.0 * 6372.7982 * 2.0 * np.pi
    DegToRad = np.pi / 180.0

    _defaultScaleVisualization = {
        21: 5,
        20: 10,
        19: 20,
        18: 20,
        17: 50,
        16: 100,
        15: 200,
        14: 500,
        13: 1 * 1000,
        12: 2 * 1000,
        11: 5 * 1000,
        10: 10 * 1000,
        9: 20 * 1000,
        8: 50 * 1000,
        7: 100 * 1000,
        6: 200 * 1000,
        5: 200 * 1000,
        4: 500 * 1000,
        3: 1000 * 1000,
    }
    """dict: Default meters that will be shown within the scale for each zoom value.
    """

    _posForAnchors = {
        Qt.TopLeftCorner: QPointF(20.0, 15.0),
        Qt.TopRightCorner: QPointF(20.0, -15.0),
        Qt.BottomLeftCorner: QPointF(20.0, -15.0),
        Qt.BottomRightCorner: QPointF(20.0, 15.0),
    }

    def __init__(self, textPen='black', barBrush=(190, 190, 190, 160), barPen=(190, 190, 190, 240),
                 barBrushHover=(110, 110, 110, 255), barPenHover=(90, 90, 90, 255),
                 anchor=Qt.BottomRightCorner, anchorPos=None, parent=None):
        """Construct a scale bar with text on the right bottom of the map

        Keyword Args:
            textPen: QPen to use for drawing the text. Default 'black'.
            barBrush: QBrush to use for drawing the scale bar. Default (190, 190, 190, 160)
            barPen: QPen to use for drawing the scale bar border. Default (190, 190, 190, 240)
            barBrushHover:  QBrush to use for drawing the scale bar when the mouse is over it.
                Default (110, 110, 110, 255).
            barPenHover: QPen to use for drawing the scale bar borderwhen the mouse is over it.
                Default (90, 90, 90, 255).
            parent: Parent item
            anchor (Qt.Corner): The *corner* used as anchor for the item, Valid values are within the
                Qt.Corner enum
            anchorPos (QPointF): The distance between the item and the *corner*

        Note:
            Almost all the argumnets accepted by the functions.makeBrush() and functions.makePen()
            are accepted.
        """
        QGraphicsObject.__init__(self, parent=parent)
        MapItem.__init__(self)

        self.setZValue(100)

        self._textPen = makePen(textPen)
        self._barBrush = makeBrush(barBrush)
        self._barPen = makePen(barPen)
        self._barBrushHover = makeBrush(barBrushHover)
        self._barPenHover = makePen(barPenHover)

        self._scaleView = MapScaleItem._defaultScaleVisualization.copy()
        self._minZoomScale = min(self._scaleView.keys())
        self._maxZoomScale = max(self._scaleView.keys())

        self.setAcceptHoverEvents(True)
        self._hover = False

        if anchorPos is None:
            anchorPos = self._posForAnchors[anchor]
        self._anchorPos = QPointF(anchorPos)
        self._anchor = anchor

        self._barWidth = 0  # The width of the scale bar
        self._text = ''  # The text to display near the scale bar
        self._zoom = 0  # The current zoom level
        self._meters = 0  # The number of meters used to evaluate the size of the scale bar and its text
        self._meterPerPixelsEquator = 0  # The number of meters each pixel represents at the equator
        self._textRect = QRectF()  # The bounding rect of text

    def _sceneChanged(self, oldScene, newScene):
        if oldScene is not None:
            oldScene.sceneRectChanged.disconnect(self._setSceneRect)
        if newScene is not None:
            newScene.sceneRectChanged.connect(self._setSceneRect)
            # Setup the new position of the item
            self.setZoom(newScene.zoom())
            self._setSceneRect(newScene.sceneRect())

    def updatePosition(self, scene):
        # Nothing to do here
        pass

    def boundingRect(self):
        anchor = self._anchor
        if anchor == Qt.BottomRightCorner or anchor == Qt.TopRightCorner:
            return QRectF(0, 0, self._barWidth + 3, 10).united(self._textRect)
        else:
            textRect = self._textRect.translated(self._barWidth + 10, 0)
            return QRectF(0, 0, self._barWidth + 3, 10).united(textRect)

    def paint(self, painter, option, widget):
        if self._hover:
            painter.setPen(self._barPenHover)
            painter.setBrush(self._barBrushHover)
        else:
            painter.setPen(self._barPen)
            painter.setBrush(self._barBrush)
        painter.drawRoundedRect(0, 0, self._barWidth, 10, 3, 3)

        anchor = self._anchor
        if anchor == Qt.BottomRightCorner or anchor == Qt.TopRightCorner:
            textRect = self._textRect
        else:
            textRect = self._textRect.translated(self._barWidth + 10, 0)
        painter.setPen(self._textPen)
        painter.drawText(textRect, Qt.TextSingleLine, self._text)

    @Slot(QRectF)
    def _setSceneRect(self, rect):
        self._updateScaleBar()

        anchorPos = self._anchorPos
        anchor = self._anchor
        newPos = None
        if anchor == Qt.BottomRightCorner:
            newPos = rect.bottomRight() - anchorPos - QPointF(self._barWidth, 0.0)
        elif anchor == Qt.TopRightCorner:
            newPos = rect.topRight() - anchorPos - QPointF(self._barWidth, 0.0)
        elif anchor == Qt.TopLeftCorner:
            newPos = rect.topLeft() + anchorPos
        elif anchor == Qt.BottomLeftCorner:
            newPos = rect.bottomLeft() + anchorPos
        else:
            raise NotImplementedError('Other corner have not actually been implemented')

        self.setPos(newPos)

    def _updateScaleBar(self):
        scene = self.scene()
        if scene is None:
            self.setVisible(False)
            return
        self.setVisible(True)

        centerYRad = scene.center().y() * self.DegToRad
        meterPerPixels = self._meterPerPixelsEquator * np.cos(centerYRad)
        self._barWidth = int(self._meters / meterPerPixels)

    def setZoom(self, zoom):
        '''Set a new zoom level.
        Args:
            zoom (int): The new zoom level.
        '''
        self._zoom = zoom
        zoomSelector = clip(zoom, self._minZoomScale, self._maxZoomScale)
        meters = self._scaleView[zoomSelector]
        if meters >= 1000:
            self._text = '%d km' % (meters / 1000.0)
        else:
            self._text = '%d m' % meters
        self._meters = meters
        self._meterPerPixelsEquator = self.EarthCircumference / np.power(2.0, zoom + 8)

        # Evaluate the bounding box of the current text
        anchor = self._anchor
        textRect = QFontMetrics(QFont()).boundingRect(self._text)
        if anchor == Qt.BottomRightCorner or anchor == Qt.TopRightCorner:
            textRect.moveLeft(-textRect.width() - 10)
            textRect.moveTop(-textRect.height() + 10)
        else:
            textRect.moveTop(-textRect.height() + 14)
        self._textRect = QRectF(textRect)
        self.update()

    def setScaleForZoom(self, zoomLevel, metersInScaleBar):
        """Set the scale in meters/kilometers to be shown for a zoom level

        Args:
            zoomLevel(int): Level of the zoom
            metersInScaleBar(int): Meters to be shown in the scale bar
        """
        if zoomLevel > self._maxZoomScale + 1:
            raise ValueError('zoomLevel must be at least %d' % (self._maxZoomScale + 1))
        if zoomLevel < self._minZoomScale - 1:
            raise ValueError('zoomLevel must be at minimum %d' % (self._minZoomScale + 1))

        self._scaleView[zoomLevel] = metersInScaleBar
        self._minZoomScale = min(self._scaleView.keys())
        self._maxZoomScale = max(self._scaleView.keys())

        # Re-evaluate the scale bar for the current zoom
        self.setZoom(self._zoom)

        self.update()

    def restoreDefaultScaleLevels(self):
        """Restore the default meter scale for the zoom levels
        """
        self._scaleView = MapScaleItem._defaultScaleVisualization.copy()
        self._minZoomScale = min(self._scaleView.keys())
        self._maxZoomScale = max(self._scaleView.keys())

        # Re-evaluate the scale bar for the current zoom
        self.setZoom(self._zoom)

        self.update()

    def setColors(self, **kwargs):
        """Set a new color for the scale bar and the text

        Keyword Args:
            textPen: QPen to use for drawing the text. Default do not change.
            barBrush: QBrush to use for drawing the scale bar. Default do not change.
            barPen: QPen to use for drawing the scale bar border.Default do not change.
            barBrushHover:  QBrush to use for drawing the scale bar when the mouse is over it.
                Default do not change.
            barPenHover: QPen to use for drawing the scale bar borderwhen the mouse is over it.
                Default do not change.
        """
        if 'textPen' in kwargs:
            self._textPen = makePen(kwargs['textPen'])
        if 'barBrush' in kwargs:
            self._barBrush = makeBrush(kwargs['barBrush'])
        if 'barPen' in kwargs:
            self._barPen = makePen(kwargs['barPen'])
        if 'barBrushHover' in kwargs:
            self._barBrushHover = makeBrush(kwargs['barBrushHover'])
        if 'barPenHover' in kwargs:
            self._barPenHover = makePen(kwargs['barPenHover'])
        self.update()

    def hoverEnterEvent(self, event):
        event.accept()
        self._hover = True
        self.update()

    def hoverLeaveEvent(self, event):
        event.accept()
        self._hover = False
        self.update()
