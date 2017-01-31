from classes import SignalPoint
from functions.basicfunctions import measure
from global_variables import tup_min_dist, tup_max_dist


def check_3_points_and_add(loc1, loc2, loc3, tuple3, label1, label2, label3):
    point_dist1 = measure(loc1[0], loc1[1], loc2[0], loc2[1])
    point_dist2 = measure(loc1[0], loc1[1], loc3[0], loc3[1])
    point_dist3 = measure(loc3[0], loc3[1], loc2[0], loc2[1])
    if tup_min_dist < point_dist1 < tup_max_dist:
        if tup_min_dist < point_dist2 < tup_max_dist:
            if tup_min_dist < point_dist3 < tup_max_dist:
                sp1 = SignalPoint()
                sp1.new_point(loc1[0], loc1[1], label1)
                sp2 = SignalPoint()
                sp2.new_point(loc2[0], loc2[1], label2)
                sp3 = SignalPoint()
                sp3.new_point(loc3[0], loc3[1], label3)
                tuple3.append([sp1, sp2, sp3])
    return tuple3

def get_3_tuple(matrix, labels):
    # add clustering to this
    # use lst instead of matrix and labels
    tuple3 = []
    for i in range(0, len(matrix)-2):
        for j in range(i+1, len(matrix)-1):
            for k in range(j+1, len(matrix)):
                tuple3 =  check_3_points_and_add(matrix[i], matrix[j], matrix[k], tuple3, labels[i], labels[j], labels[j])
    return tuple3

'''def eliminate_outliers(matrix, labels):
    # add clustering to this
    # use lst instead of matrix and labels
    tuple3 = []
    leng = len(matrix)
    cnt = 0
    for i in range(0, leng-1):
        out = 1
        for j in range(i+1, leng):
            if(isAnOutlier(matrix[i], matrix[j], labels, i, j) == False):
                out = 0
                break
        if(out == 1):
            del labels[i]
            del matrix[i]
            i -= 1
            cnt += 1
            leng -= 1
        print (str(i) + " " + str(leng))

    return cnt
'''

