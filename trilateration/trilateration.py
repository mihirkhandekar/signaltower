# http://stackoverflow.com/questions/9747227/2d-
# http://stackoverflow.com/questions/3472469/trilateration-in-a-2d-plane-with-signal-strengths?rq=1
# http://gis.stackexchange.com/questions/40660/trilateration-algorithm-for-n-amount-of-points
# http://gis.stackexchange.com/questions/66/trilateration-using-3-latitude-and-longitude-points-and-3-distances

from functions.basicfunctions import measure
from global_variables import signal_factor, max_signal, division_factor, max_range

def trilaterate(x1, y1, x2, y2, x3, y3, s1, s2, s3):
    import math
    import numpy
    s1 = signal_factor * (max_signal - s1)
    s2 = signal_factor * (max_signal - s2)
    s3 = signal_factor * (max_signal - s3)

    # assuming elevation = 0
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
        corr = False
    else:
        corr = True

    return corr, lat, lon


