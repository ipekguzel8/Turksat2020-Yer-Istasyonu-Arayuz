from __future__ import print_function, absolute_import

from .maptilesourcehttp import MapTileSourceHTTP


class MapTileSourceHereDemo(MapTileSourceHTTP):

    _server = None

    def __init__(self, tileSize=256, parent=None):
        MapTileSourceHTTP.__init__(self, tileSize=tileSize, minZoom=2, maxZoom=20, parent=parent)
        assert tileSize == 256 or tileSize == 512
        self._server = 0

    def url(self, x, y, zoom):
        self._server += 1
        if self._server > 4:
            self._server = 0
        url = "http://%d.base.maps.cit.api.here.com/maptile/2.1/maptile/" % self._server
        url += "newest/normal.day/%d/%d/%d/%d/png8" % (zoom, x, y, self._tileSize)
        url += '?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg'
        return url


class MapTileSourceHere(MapTileSourceHTTP):

    def __init__(self, tileSize=256, app_id='DemoAppId01082013GAL', app_code='AJKnXv84fjrb0KIHawS0Tg',
                 scheme='normal.day', cit=True, tileType='maptile', mapType='base', imageFmt='png8',
                 userAgent='(PyQt) TileMap 1.0 - HERE', mapHttpLoader=None,
                 minZoom=2, maxZoom=20, parent=None):
        MapTileSourceHTTP.__init__(self, tileSize=tileSize, minZoom=minZoom, maxZoom=maxZoom,
                                   mapHttpLoader=mapHttpLoader, parent=parent)
        assert tileSize == 256 or tileSize == 512
        self._server = 0

        self._app_id = app_id
        self._app_code = app_code

        self._mapType = mapType
        self._tileType = tileType
        self._scheme = scheme
        self._cit = '.cit' if cit else ''
        self._imageFmt = imageFmt

        self._buildBaseUrl()

    def _buildBaseUrl(self):
        url = 'http://%d.' + self._mapType + '.maps' + self._cit + '.api.here.com'
        url += '/maptile/2.1/' + self._tileType + '/newest/' + self._scheme + \
               '/%d/%d/%d/' + str(self._tileSize) + '/' + self._imageFmt
        url += '?app_id=%s&app_code=%s' % (self._app_id, self._app_code)
        self._baseurl = url

    def setOptions(self, scheme=None, tileType=None, mapType=None):
        if mapType is not None:
            self._mapType = mapType
        if tileType is not None:
            self._tileType = tileType
        if scheme is not None:
            self._scheme = scheme

        self._buildBaseUrl()

    def url(self, x, y, zoom):
        self._server += 1
        if self._server > 4:
            self._server = 0

        args = (self._server, zoom, x, y)
        url = self._baseurl % args
        return url
