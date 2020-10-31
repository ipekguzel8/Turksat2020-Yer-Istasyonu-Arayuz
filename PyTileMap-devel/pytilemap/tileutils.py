from __future__ import division

import numpy as np
from numpy import log, tan, cos, arctan, exp
from numpy import pi as PI


Deg2Rad = PI / 180.0
PI2 = PI * 2.0


def posFromLonLat(lon, lat, zoom, tileSize):
    """Position in scene coordinate of the WGS84 coordinates.

    Convert from WGS84 reference system to scene reference system.

    Args:
        lon(float or numpy.ndarray): Longitude value or values.
        lat(float or numpy.ndarray): Latitude value or values.
        zoom(int): The zoom level.
        tileSize(int): The size of the tile.

    Returns:
        tuple: (x, y) with the positions of the input coordinates.
    """
    if isinstance(lat, np.ndarray):
        return _posFromLonLatArray(lon, lat, zoom, tileSize)

    tx = lon + 180.0
    tx /= 360.0
    ty = (1.0 - log(tan(lat * Deg2Rad) + 1.0 / cos(lat * Deg2Rad)) / PI) / 2.0
    zn = (1 << zoom) * float(tileSize)
    tx *= zn
    ty *= zn
    return tx, ty


def _posFromLonLatArray(lon, lat, zoom, tileSize):
    # Optimized implementation of posFromLonLat() function for numpy arrays
    tx = lon + 180.0
    tx /= 360.0

    tmp = lat * Deg2Rad
    ty = cos(tmp)
    np.divide(1.0, ty, out=ty)
    tan(tmp, out=tmp)
    ty += tmp
    log(ty, out=ty)
    ty /= PI
    np.subtract(1.0, ty, out=ty)
    ty /= 2.0

    zn = (1 << zoom) * float(tileSize)
    tx *= zn
    ty *= zn
    return tx, ty


def lonLatFromPos(x, y, zoom, tileSize):
    """Position in WGS84 coordinate of the scene coordinates.

    Convert from scene reference system to WGS84 reference system.

    Args:
        x(float, int or numpy.ndarray): X value or values.
        y(float, int or numpy.ndarray): Y value or values.
        zoom(int): The zoom level.
        tileSize(int): The size of the tile.

    Returns:
        tuple: (lon, lat) with the coordinates of the input positions.
    """
    if isinstance(y, np.ndarray):
        return _lonLatFromPosArray(x, y, zoom, tileSize)

    tx = x / tileSize
    ty = y / tileSize
    zn = 1 << zoom
    lon = tx / zn * 360.0 - 180.0
    n = PI - PI2 * ty / zn
    lat = arctan(0.5 * (exp(n) - exp(-n))) / Deg2Rad
    return lon, lat


def _lonLatFromPosArray(x, y, zoom, tileSize):
    # Optimized implementation of posFromLonLat() function for numpy arrays
    zn = 1 << zoom

    lon = x / tileSize
    lon /= zn
    lon *= 360
    lon -= 180

    lat = y / tileSize
    lat *= -PI2 / zn
    lat += PI
    tmp = lat * -1.0
    exp(lat, out=lat)
    exp(tmp, out=tmp)
    lat -= tmp
    lat *= 0.5
    arctan(lat, out=lat)
    lat /= Deg2Rad

    return lon, lat
