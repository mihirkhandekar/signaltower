import math


def measure(lat1, lon1, lat2, lon2):
    R = 6378.137  # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000  # meters

def get_all_signal_points_arrays(matrix):
    xtows = []
    ytows = []
    labels = []
    for row in matrix:
        xtows.append(row[0])
        ytows.append(row[1])
    for lab in labels:
        labels.append(lab)

    return xtows, ytows, labels

def combine_separate_latlon(xcents, ycents):
    clust_matrix = []
    xlen = len(xcents)
    ylen = len(ycents)
    if(xlen != ylen):
        return None
    for i in range(0, xlen):
        row_matrix = []
        row_matrix.append(xcents[i])
        row_matrix.append(ycents[i])

        clust_matrix.append(row_matrix)

    return clust_matrix
