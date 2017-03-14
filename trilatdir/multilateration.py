# https://pypi.python.org/pypi/Localization/0.1.4
import numpy as np
import numpy
from math import sin, cos, atan, tan
import math
import localization

wgs84_geoid = numpy.array([[13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
                            13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],  # 90N
                           [3, 1, -2, -3, -3, -3, -1, 3, 1, 5, 9, 11, 19, 27, 31, 34, 33, 34, 33, 34, 28, 23, 17, 13, 9,
                            4, 4, 1, -2, -2, 0, 2, 3, 2, 1, 1],  # 80N
                           [2, 2, 1, -1, -3, -7, -14, -24, -27, -25, -19, 3, 24, 37, 47, 60, 61, 58, 51, 43, 29, 20, 12,
                            5, -2, -10, -14, -12, -10, -14, -12, -6, -2, 3, 6, 4],  # 70N
                           [2, 9, 17, 10, 13, 1, -14, -30, -39, -46, -42, -21, 6, 29, 49, 65, 60, 57, 47, 41, 21, 18,
                            14, 7, -3, -22, -29, -32, -32, -26, -15, -2, 13, 17, 19, 6],  # 60N
                           [-8, 8, 8, 1, -11, -19, -16, -18, -22, -35, -40, -26, -12, 24, 45, 63, 62, 59, 47, 48, 42,
                            28, 12, -10, -19, -33, -43, -42, -43, -29, -2, 17, 23, 22, 6, 2],  # 50N
                           [-12, -10, -13, -20, -31, -34, -21, -16, -26, -34, -33, -35, -26, 2, 33, 59, 52, 51, 52, 48,
                            35, 40, 33, -9, -28, -39, -48, -59, -50, -28, 3, 23, 37, 18, -1, -11],  # 40N
                           [-7, -5, -8, -15, -28, -40, -42, -29, -22, -26, -32, -51, -40, -17, 17, 31, 34, 44, 36, 28,
                            29, 17, 12, -20, -15, -40, -33, -34, -34, -28, 7, 29, 43, 20, 4, -6],  # 30N
                           [5, 10, 7, -7, -23, -39, -47, -34, -9, -10, -20, -45, -48, -32, -9, 17, 25, 31, 31, 26, 15,
                            6, 1, -29, -44, -61, -67, -59, -36, -11, 21, 39, 49, 39, 22, 10],  # 20N
                           [13, 12, 11, 2, -11, -28, -38, -29, -10, 3, 1, -11, -41, -42, -16, 3, 17, 33, 22, 23, 2, -3,
                            -7, -36, -59, -90, -95, -63, -24, 12, 53, 60, 58, 46, 36, 26],  # 10N
                           [22, 16, 17, 13, 1, -12, -23, -20, -14, -3, 14, 10, -15, -27, -18, 3, 12, 20, 18, 12, -13,
                            -9, -28, -49, -62, -89, -102, -63, -9, 33, 58, 73, 74, 63, 50, 32],  # 0
                           [36, 22, 11, 6, -1, -8, -10, -8, -11, -9, 1, 32, 4, -18, -13, -9, 4, 14, 12, 13, -2, -14,
                            -25, -32, -38, -60, -75, -63, -26, 0, 35, 52, 68, 76, 64, 52],  # 10S
                           [51, 27, 10, 0, -9, -11, -5, -2, -3, -1, 9, 35, 20, -5, -6, -5, 0, 13, 17, 23, 21, 8, -9,
                            -10, -11, -20, -40, -47, -45, -25, 5, 23, 45, 58, 57, 63],  # 20S
                           [46, 22, 5, -2, -8, -13, -10, -7, -4, 1, 9, 32, 16, 4, -8, 4, 12, 15, 22, 27, 34, 29, 14, 15,
                            15, 7, -9, -25, -37, -39, -23, -14, 15, 33, 34, 45],  # 30S
                           [21, 6, 1, -7, -12, -12, -12, -10, -7, -1, 8, 23, 15, -2, -6, 6, 21, 24, 18, 26, 31, 33, 39,
                            41, 30, 24, 13, -2, -20, -32, -33, -27, -14, -2, 5, 20],  # 40S
                           [-15, -18, -18, -16, -17, -15, -10, -10, -8, -2, 6, 14, 13, 3, 3, 10, 20, 27, 25, 26, 34, 39,
                            45, 45, 38, 39, 28, 13, -1, -15, -22, -22, -18, -15, -14, -10],  # 50S
                           [-45, -43, -37, -32, -30, -26, -23, -22, -16, -10, -2, 10, 20, 20, 21, 24, 22, 17, 16, 19,
                            25, 30, 35, 35, 33, 30, 27, 10, -2, -14, -23, -30, -33, -29, -35, -43],  # 60S
                           [-61, -60, -61, -55, -49, -44, -38, -31, -25, -16, -6, 1, 4, 5, 4, 2, 6, 12, 16, 16, 17, 21,
                            20, 26, 26, 22, 16, 10, -1, -16, -29, -36, -46, -55, -54, -59],  # 70S
                           [-53, -54, -55, -52, -48, -42, -38, -38, -29, -26, -26, -24, -23, -21, -19, -16, -12, -8, -4,
                            -1, 1, 4, 4, 6, 5, 4, 2, -6, -15, -24, -33, -40, -48, -50, -53, -52],  # 80S
                           [-30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30,
                            -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30]],
                          # 90S
                          dtype=numpy.float)




# WGS84 reference ellipsoid constants
wgs84_a = 6378137.0
wgs84_b = 6356752.314245
wgs84_e2 = 0.0066943799901975848
wgs84_a2 = wgs84_a ** 2  # to speed things up a bit
wgs84_b2 = wgs84_b ** 2

def ecef2llh((x, y, z)):
    ep = math.sqrt((wgs84_a2 - wgs84_b2) / wgs84_b2)
    p = math.sqrt(x ** 2 + y ** 2)
    th = math.atan2(wgs84_a * z, wgs84_b * p)
    lon = math.atan2(y, x)
    lat = math.atan2(z + ep ** 2 * wgs84_b * math.sin(th) ** 3, p - wgs84_e2 * wgs84_a * math.cos(th) ** 3)
    N = wgs84_a / math.sqrt(1 - wgs84_e2 * math.sin(lat) ** 2)
    alt = p / math.cos(lat) - N

    lon *= (180. / math.pi)
    lat *= (180. / math.pi)

    return [lat, lon, alt]



def mul1(P, dists):
    R = 6378137  # Earth radius in meters
    A = []
    for m in range(0, len(P)):
        x = P[m][0]
        y = P[m][1]
        z = P[m][2]
        Am = -2 * x
        Bm = -2 * y
        Cm = -2 * z
        Dm = R * R + (pow(x, 2) + pow(y, 2) + pow(z, 2)) - pow(dists[m], 2)
        A += [[Am, Bm, Cm, Dm]]
    # Solve using SVD
    A = numpy.array(A)
    (_, _, v) = numpy.linalg.svd(A)
    # Get the minimizer
    w = v[3, :]
    w /= w[3]  # Resulting position in ECEF


# http://stackoverflow.com/questions/10473852/convert-latitude-and-longitude-to-point-in-3d-space
def llarToWorld(lat, lon, alt, rad=6378137):
    # see: http://www.mathworks.de/help/toolbox/aeroblks/llatoecefposition.html
    f  = 0                              # flattening
    ls = atan((1 - f)**2 * tan(lat))    # lambda

    x = rad * cos(ls) * cos(lon) + alt * cos(lat) * cos(lon)
    y = rad * cos(ls) * sin(lon) + alt * cos(lat) * sin(lon)
    z = rad * sin(ls) + alt * sin(lat)

    return x, y, z

def lltoecef(lat, lon, altitude, radius=6378137):
    r = radius + altitude
    x = r * cos(lon) * sin(lat)
    y = r * sin(lon) * sin(lat)
    z = r * cos(lat)
    return x, y, z


def LLHtoECEF(lat, lon, alt):
    # see http://www.mathworks.de/help/toolbox/aeroblks/llatoecefposition.html

    rad = np.float64(6378137.0)  # Radius of the Earth (in meters)
    f = np.float64(1.0 / 298.257223563)  # Flattening factor WGS84 Model
    cosLat = np.cos(lat)
    sinLat = np.sin(lat)
    FF = (1.0 - f) ** 2
    C = 1 / np.sqrt(cosLat ** 2 + FF * sinLat ** 2)
    S = C * FF

    x = (rad * C + alt) * cosLat * np.cos(lon)
    y = (rad * C + alt) * cosLat * np.sin(lon)
    z = (rad * S + alt) * sinLat

    return (x, y, z)

# http://www.oc.nps.edu/oc2902w/coord/llhxyz.htm TO VERIFY

# Multilateration ::::: http://stackoverflow.com/questions/17756617/finding-an-unknown-point-using-weighted-multilateration

print str(ecef2llh(LLHtoECEF(18.5240946395,73.8278497199, 0)))
print str(ecef2llh(lltoecef(18.5240946395,73.8278497199, 0)))
print str(ecef2llh(llarToWorld(18.5240946395,73.8278497199, 0)))


'''P.add_anchor('1',(18.530143, 73.854764))
P.add_anchor('2',(18.530835, 73.856097))
P.add_anchor('3',(18.530637, 73.857547))'''
