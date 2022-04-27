from functions.basicfunctions import measure
from global_variables import tup_min_dist, tup_max_dist
from trilatdir.trilateration import trilaterate

def check_2_points(loc1, loc2):
    return (
        tup_min_dist
        < measure(loc1[0], loc1[1], loc2[0], loc2[1])
        < tup_max_dist
    )

def get_tower_locations_trilaterate(matrix, labels):
    count = 0
    xcents = []
    ycents = []

    for i in range(len(matrix) - 2):
        for j in range(i + 1, len(matrix) - 1):
            if (check_2_points(matrix[i], matrix[j])):
                for k in range(j + 1, len(matrix)):
                    # thread.start_new_thread(check_3_points_and_add, (matrix[i], matrix[j], matrix[k], tuple3, labels[i], labels[j], labels[j]))
                    if (check_2_points(matrix[i], matrix[k]) and check_2_points(matrix[j], matrix[k])):
                        corr, x1, y1 = trilaterate(matrix[i][0], matrix[i][1],
                                                   matrix[j][0], matrix[j][1],
                                                   matrix[k][0], matrix[k][1],
                                                   labels[i], labels[j],
                                                   labels[k])
                        if corr == True:
                            xcents.append(x1)
                            ycents.append(y1)
                            count += 1

    return xcents, ycents, count


def get_tower_locations_multilaterate(matrix, labels):
    count = 0
    i = 0
    tuplist = []
    for i in range(len(matrix)):
        for _ in range(i + 1, len(matrix)):
            tuplist.append()


def get_tower_locations(matrix, labels, lateration='tri'):
    if lateration == 'tri':
        xcents, ycents, count = get_tower_locations_trilaterate(matrix, labels)
        return xcents, ycents, count
    elif lateration == 'multi':
        xcents, ycents, count = get_tower_locations_multilaterate(matrix, labels)
        return xcents, ycents, count




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
