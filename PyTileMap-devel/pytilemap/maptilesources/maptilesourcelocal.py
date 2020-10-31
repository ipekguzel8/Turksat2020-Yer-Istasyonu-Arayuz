from __future__ import print_function, absolute_import

import os

from qtpy.QtGui import QPixmap

from .maptilesource import MapTileSource


class MapTileSourceDirectory(MapTileSource):

    _directory = None
    _fnameSuffix = None

    def __init__(self, directory, filenameSuffix='.png', tileSize=256, minZoom=2, maxZoom=18, parent=None):
        MapTileSource.__init__(self, tileSize=tileSize, minZoom=minZoom, maxZoom=maxZoom, parent=parent)
        self._directory = directory
        self._fnameSuffix = filenameSuffix

    def tileSize(self):
        return self._tileSize

    def maxZoom(self):
        return self._maxZoom

    def minZoom(self):
        return self._minZoom

    def requestTile(self, x, y, zoom):
        filename = os.path.join(self._directory, str(zoom), str(x), str(y)+self._fnameSuffix)
        if os.path.exists(filename):
            return QPixmap(filename)
        return None
