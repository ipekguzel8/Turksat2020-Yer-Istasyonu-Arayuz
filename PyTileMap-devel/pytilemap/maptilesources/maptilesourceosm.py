from __future__ import print_function, absolute_import

from .maptilesourcehttp import MapTileSourceHTTP


class MapTileSourceOSM(MapTileSourceHTTP):

    def __init__(self, parent=None):
        MapTileSourceHTTP.__init__(self, parent=parent)

    def url(self, x, y, zoom):
        url = "http://tile.openstreetmap.org/%d/%d/%d.png" % (zoom, x, y)
        return url
