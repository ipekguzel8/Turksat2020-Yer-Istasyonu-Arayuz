from __future__ import print_function, absolute_import

from qtpy.QtCore import Signal, Slot, QObject
from qtpy.QtGui import QPixmap


class MapTileSource(QObject):

    tileReceived = Signal(int, int, int, QPixmap)

    _tileSize = None
    _minZoom = None
    _maxZoom = None

    def __init__(self, tileSize=256, minZoom=2, maxZoom=18, parent=None):
        QObject.__init__(self, parent=parent)
        self._tileSize = tileSize
        self._minZoom = minZoom
        self._maxZoom = maxZoom

    def tileSize(self):
        return self._tileSize

    def maxZoom(self):
        return self._maxZoom

    def minZoom(self):
        return self._minZoom

    def requestTile(self, x, y, zoom):
        raise NotImplementedError()

    @Slot()
    def abortAllRequests(self):
        pass

    @Slot()
    def close(self):
        pass
