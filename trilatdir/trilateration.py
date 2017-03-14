# http://stackoverflow.com/questions/9747227/2d-
# http://stackoverflow.com/questions/3472469/trilateration-in-a-2d-plane-with-signal-strengths?rq=1
# http://gis.stackexchange.com/questions/40660/trilateration-algorithm-for-n-amount-of-points
# http://gis.stackexchange.com/questions/66/trilateration-using-3-latitude-and-longitude-points-and-3-distances

from functions.basicfunctions import measure
from global_variables import signal_factor, max_signal, division_factor, max_range
import math
import numpy, numpy as np
import scipy.optimize as opt



def trilaterate(x1, y1, x2, y2, x3, y3, s1, s2, s3):
    s1 = signal_factor * (max_signal - s1)
    s2 = signal_factor * (max_signal - s2)
    s3 = signal_factor * (max_signal - s3)

    earthR = 6371
    LatA = x1
    LonA = y1
    DistA = s1 / division_factor
    LatB = x2
    LonB = y2
    DistB = s2 / division_factor
    LatC = x3
    LonC = y3
    DistC = s3 / division_factor

    xA = earthR * (math.cos(math.radians(LatA)) * math.cos(math.radians(LonA)))
    yA = earthR * (math.cos(math.radians(LatA)) * math.sin(math.radians(LonA)))
    zA = earthR * (math.sin(math.radians(LatA)))

    xB = earthR * (math.cos(math.radians(LatB)) * math.cos(math.radians(LonB)))
    yB = earthR * (math.cos(math.radians(LatB)) * math.sin(math.radians(LonB)))
    zB = earthR * (math.sin(math.radians(LatB)))

    xC = earthR * (math.cos(math.radians(LatC)) * math.cos(math.radians(LonC)))
    yC = earthR * (math.cos(math.radians(LatC)) * math.sin(math.radians(LonC)))
    zC = earthR * (math.sin(math.radians(LatC)))

    P1 = numpy.array([xA, yA, zA])
    P2 = numpy.array([xB, yB, zB])
    P3 = numpy.array([xC, yC, zC])

    ex = (P2 - P1) / (numpy.linalg.norm(P2 - P1))
    i = numpy.dot(ex, P3 - P1)
    ey = (P3 - P1 - i * ex) / (numpy.linalg.norm(P3 - P1 - i * ex))

    d = numpy.linalg.norm(P2 - P1)
    j = numpy.dot(ey, P3 - P1)

    x = (pow(DistA, 2) - pow(DistB, 2) + pow(d, 2)) / (2 * d)
    y = ((pow(DistA, 2) - pow(DistC, 2) + pow(i, 2) + pow(j, 2)) / (2 * j)) - ((i / j) * x)

    triPt = P1 + x * ex + y * ey

    lat = math.degrees(math.asin(triPt[2] / earthR))
    lon = math.degrees(math.atan2(triPt[1], triPt[0]))

    if measure(lat, lon, LatA, LonA) > max_range or measure(lat, lon, LatB, LonB) > max_range or measure(lat, lon, LatC, LonC) > max_range:
        return False, lat, lon
    else:
        return True, lat, lon


#####################################
# Multilateration
#####################################
earth_radius = 6378.137
#Returns the distance from a point to the list of spheres
def calc_distance(point):
    return np.power(np.sum(np.power(centers-point,2),axis=1),.5)-rad

#Latitude/longitude to carteisan
def geo2cart(lat,lon):
    lat=np.deg2rad(lat)
    lon=np.deg2rad(lon)
    points=np.vstack((earth_radius*np.cos(lat)*np.cos(lon),
           earth_radius*np.cos(lat)*np.sin(lon),
           earth_radius*np.sin(lat))).T
    return points

#Cartesian to lat/lon
def cart2geo(xyz):
    if xyz.ndim==1: xyz=xyz[None,:]
    lat=np.arcsin(xyz[:,2]/earth_radius)
    lon=np.arctan2(xyz[:,1],xyz[:,0])
    return np.rad2deg(lat),np.rad2deg(lon)

#Minimization function.
def minimize(point):
    dist= calc_distance(point)
    #Here you can change the minimization parameter, here the distances
    #from a sphere to a point is divided by its radius for linear weighting.
    err=np.linalg.norm(dist/rad)
    return err

def multilaterate(p):

    points = np.vstack(p)
    lat = points[:, 0]
    lon = points[:, 1]
    rad = points[:, 2]

    centers = geo2cart(lat, lon)

    out = []
    for x in range(30):
        latrand = np.average(lat / rad) * np.random.rand(1) * np.sum(rad)
        lonrand = np.average(lon / rad) * np.random.rand(1) * np.sum(rad)
        start = geo2cart(latrand, lonrand)
        end_pos = opt.fmin_powell(minimize, start)
        out.append([cart2geo(end_pos), np.linalg.norm(end_pos - geo2cart(36.989, 91464))])

    out = sorted(out, key=lambda x: x[1])
    print out[0][0][0][0], ',', out[0][0][1][0], 'Distance:', out[0][1]

