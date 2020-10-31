import pytest
import numpy as np

from pytilemap.tileutils import posFromLonLat, lonLatFromPos


LATITUDES = np.arange(-90, 90).astype(np.float64)
LONGITUDES = np.arange(-180, 180).astype(np.float64)
ZOOMS = np.arange(1, 20).astype(np.int64)


def referencePosFromLonLat(lon, lat, zoom, tileSize):
    tx = (lon + 180.0) / 360.0
    ty = (1.0 - np.log(np.tan(np.deg2rad(lat)) + 1.0 / np.cos(np.deg2rad(lat))) / np.pi) / 2.0
    zn = (1 << zoom) * float(tileSize)
    tx *= zn
    ty *= zn
    return tx, ty


def referenceLonLatFromPos(x, y, zoom, tileSize):
    tx = x / tileSize
    ty = y / tileSize
    zn = 1 << zoom
    lon = tx / zn * 360.0 - 180.0
    n = np.pi - np.pi * 2. * ty / zn
    lat = np.rad2deg(np.arctan(0.5 * (np.exp(n) - np.exp(-n))))
    return lon, lat


@pytest.mark.parametrize('lons,lats,zooms', [(LONGITUDES[::2], LATITUDES[::2], ZOOMS[::2])])
def test_posFromLonLat_viceversa(lons, lats, zooms):
    for lon in lons:
        for lat in lats:
            for zoom in zooms:
                tx, ty = posFromLonLat(lon, lat, zoom, 256)
                refTx, refTy = posFromLonLat(lon, lat, zoom, 256)
                assert tx == refTx
                assert ty == refTy

                ll = lonLatFromPos(tx, ty, zoom, 256)
                assert abs(ll[0] - lon) < 1e-13
                assert abs(ll[1] - lat) < 1e-13


@pytest.mark.parametrize('lons,lats,zooms', [(LONGITUDES, LATITUDES, ZOOMS)])
def test_posFromLonLat_viceversa_array(lons, lats, zooms):

    latitude = np.tile(lats, lons.size)
    longitude = np.repeat(lons, lats.size)

    for zoom in zooms:
        tx, ty = posFromLonLat(longitude, latitude, zoom, 256)
        refTx, refTy = posFromLonLat(longitude, latitude, zoom, 256)
        assert np.nanmax(np.abs(tx - refTx)) < 1e-12
        assert np.nanmax(np.abs(ty - refTy)) < 1e-12

        ll = lonLatFromPos(tx, ty, zoom, 256)
        assert np.nanmax(np.abs(ll[0] - longitude)) < 1e-12
        assert np.nanmax(np.abs(ll[1] - latitude)) < 1e-12
