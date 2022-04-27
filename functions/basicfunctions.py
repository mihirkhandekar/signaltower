import math
import os


def measure(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of earth in KM
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
    labels.extend(iter(labels))
    return xtows, ytows, labels

def combine_separate_latlon(xcents, ycents):
    clust_matrix = []
    xlen = len(xcents)
    ylen = len(ycents)
    if(xlen != ylen):
        return None
    for i in range(xlen):
        row_matrix = [xcents[i], ycents[i]]
        clust_matrix.append(row_matrix)

    return clust_matrix

def arffFile(xcents, ycents, provider, starttime, endtime, directory='static/download'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename='trilat_' + provider + starttime + endtime + '.arff'
    f1 = open(directory+'/' + filename, "w+")
    f1.write("%Data: Non clustered trilaterated Mobile Tower Localisation Locations" + "\n")
    f1.write("%Carrier: " + provider + "\n")
    f1.write("%Start  : " + starttime + "\n")
    f1.write("%End    : " + endtime + "\n")
    f1.write("@RELATION mobile-networks" + "\n")
    f1.write("@ATTRIBUTE latitude  NUMERIC" + "\n")
    f1.write("@ATTRIBUTE longitude  NUMERIC" + "\n")
    f1.write("@DATA" + "\n")
    for i in range(len(xcents)):
        f1.write(str(xcents[i]) + "," + str(ycents[i])  + "\n")

    print "Done writing to file"
    f1.close()
    return filename

