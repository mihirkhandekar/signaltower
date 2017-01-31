import MySQLdb

from flask import json

from classes import SignalPoint
from trilateration.trilateration import trilaterate


def get_data(carrier, starttime, endtime, offline = True):
    print()
    if offline == False:
        db = MySQLdb.connect(host="projectdb1.czthhr2kqju8.us-east-1.rds.amazonaws.com",  # your host, usually localhost
                             user="mac",
                             passwd="mac113140",
                             db="sigdb")
        print("Connected to database")
        cur = db.cursor()
        carrier = carrier.replace("+", " ")
        starttime = starttime.replace("+", " ")
        endtime = endtime.replace("+", " ")
        starttime = starttime.replace("%3A", ":")
        endtime = endtime.replace("%3A", ":")
        # Use all the SQL you like
        query = "SELECT * FROM sigtab where "
        query += ("carrier = '" + carrier + "' ")
        if starttime is not None and starttime != "":
            query += ("and time > '" + starttime + "' ")
        if endtime is not None and endtime != "":
            query += ("and time < '" + endtime + "' ")
        cur.execute(query)
        lst = []
        matrix = []
        labels = []

        i = 0
        for row in cur.fetchall():
            rowmat = []
            rowmat.append(float(row[0]))
            rowmat.append(float(row[1]))
            matrix.append(rowmat)

            labels.append(int(row[2]))

            rowlst = SignalPoint()
            rowlst.new_point(float(row[0]), float(row[1]), int(row[2]))

            i += 1

        db.close()
        print "Returned " + str(i) + " rows."
        return lst, matrix, labels


    with open(r'/home/mihir/PycharmProjects/ocid/main/jsonfiles/airtel220117.json') as jsondata:
        data = json.load(jsondata)
        w = 3
        length = len(data["data"])
        lst = [SignalPoint() for i in range(length)]
        matrix = [[0 for x in range(w)] for y in range(length)]
        labels = []
        i = 0
        for row in data["data"]:
            lst[i].new_point(row["lat"], row["lon"], row["signal"])
            matrix[i][0] = float(row["lat"])
            matrix[i][1] = float(row["lon"])
            labels.append(int(row["signal"]))
            i += 1
        print "Returned " + str(length) + " rows."
        return lst, matrix, labels

def get_tower_locations(tuple3):
    count = 0
    xcents = []
    ycents = []

    for i in range (0, len(tuple3)):

        corr, x1, y1 = trilaterate(tuple3[i][0].lat, tuple3[i][0].lon, tuple3[i][1].lat, tuple3[i][1].lon, tuple3[i][2].lat, tuple3[i][2].lon, tuple3[i][0].sig, tuple3[i][1].sig, tuple3[i][2].sig)
        if corr == True:
            xcents.append(x1)
            ycents.append(y1)
            # print str(x1) +", " + str(y1)
            count += 1

    return xcents, ycents, count
