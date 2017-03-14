import MySQLdb
import csv
import pickle
import pprint
import urllib

from datetime import datetime
from flask import json

import functions.datagenerate
import graphs.plotting
from classes import SignalPoint

def get_data(carrier, starttime, endtime, offline = True, random=True):
    print()
    if random == True:
        nooftowers = 60
        reading_tower_ratio = 15

        tlats, tlons = functions.datagenerate.gen_locations(nooftowers)
        llats, llons = functions.datagenerate.gen_locations(nooftowers * reading_tower_ratio)
        llats, llons, signal = functions.datagenerate.gen_measurements(tlats, tlons, llats, llons)
        print "signals", str(signal)

        length = len(signal)
        w = 3
        lst = [SignalPoint() for i in range(length)]
        matrix = [[0 for x in range(w)] for y in range(length)]
        labels = []
        i = 0
        for i in range(length):
            lst[i].new_point(llats[i], llons[i], signal[i])
            matrix[i][0] = float(llats[i])
            matrix[i][1] = float(llons[i])
            labels.append(int(signal[i]))
            i += 1
        print "Returned " + str(length) + " rows."
        return lst, matrix, labels, tlats, tlons
        # graphs.plotting.google_plot(tlats, tlons, llats, llons, filename="randomtows.html")



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
        query = "SELECT * FROM specialtab where "
        query += ("carrier = '" + carrier + "' ")
        if starttime is not None and starttime != "":
            query += ("and time > '" + starttime + "' ")
        if endtime is not None and endtime != "":
            query += ("and time < '" + endtime + "' ")
        print query
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

def getCentres(provider, starttime, endtime):
    provider = provider.replace(" ", "+")
    cclat = []
    cclon = []
    import urllib
    url = "https://clusteringapp.herokuapp.com/run/" + provider + "/" + starttime + "/" + endtime
    print url
    response = urllib.urlopen(url)
    data = response.read()
    data2 = data.split('<br/>')
    # print str(data2)
    for line in data2:
        # print line
        coords = line.split(',')
        if(len(coords) == 2):
            # print str(coords)
            if(coords[0] != '' and coords[1] != ''):
                cclat.append(float(coords[0]))
                cclon.append(float(coords[1]))
    # print data

    return cclat, cclon

def get_train_data():
    fname = 'datatrain.dict'

    import os.path
    if os.path.isfile(fname):
        os.chdir(r'/home/mihir/PycharmProjects/SignalTower/ml')
        # in1 = open(fname, 'r')
        (d, im) = pickle.load(open(fname, 'rb'))
        return d, im


    url0 = 'http://signalapps.herokuapp.com/getAllImei'
    print url0
    response = urllib.urlopen(url0)
    data = response.read()
    data2 = json.loads(data)
    print str(data2)
    readings = data2['data']
    imei = []
    for row in readings:
        imei.append(row['imei'])
    print str(imei)

    d = dict()
    for ime in imei:
        url = 'http://signalapps.herokuapp.com/signalsearch?starttime=2017-01-01+00:00:00&endtime=2017-03-23+00:00:00&imei=' + ime
        print url
        response = urllib.urlopen(url)
        data = response.read()
        data2 = json.loads(data)
        # print str(data2)
        readings = data2['data']
        # pprint.pprint(readings)

        matrix = []
        for row in readings:
            rowmat = []
            rowmat.append(float(row["lat"]))    # Lat
            rowmat.append(float(row["lon"]))    # Lon
            rowmat.append(str(row["time"]))      # Time
            # datetime_object = datetime.strptime(str(row[4]), '%Y-%m-%d %H:%M:%S')
            # rowmat.append(datetime_object)
            rowmat.append(str(row["imei"]))      # IMEI
            matrix.append(rowmat)

        print 'imei:', ime, 'rows:', len(matrix)
        d[ime] = matrix

    with open(fname,'wb') as f:
        pickle.dump((d, imei),f)


    print "TOTAL returned", len(d), 'imei'
    return d, imei

def draw_chart(lat, lon, sig = None, clat = None, clon = None):
    from matplotlib import pyplot as plt

    y = lon
    z = lat
    n = sig

    fig, ax = plt.subplots()
    ax.scatter(z, y, color='blue')


    if sig != None:
        for i, txt in enumerate(n):
            ax.annotate(txt, (z[i], y[i]))
    if clat != None and clon != None:
        ax.scatter(clat, clon, color='red')

    plt.show()

def plot_tower(X, Y, x, y, slist):
    xlist = X
    ylist = Y
    draw_chart(xlist, ylist, slist, x, y)

def show_on_map(lats, lons, labels, title, tlats, tlons):
    from mpl_toolkits.basemap import Basemap
    from matplotlib import pyplot as plt

    lllon = min(lons)
    lllat = min(lats)

    urlon = max(lons)
    urlat = max(lats)

    lat0 = (lllat + urlat) / 2
    lon0 = (lllon + urlon) / 2

    map = Basemap(projection='merc', lat_0=18.532901, lon_0=73.851471, epsg=4326,
                  resolution='h', area_thresh=0.1,
                             llcrnrlon=73.645477, llcrnrlat=18.346705, urcrnrlon=74.057465, urcrnrlat=18.719097)

    map.arcgisimage(service='World_Street_Map', xpixels=2000)

    x, y = map(lons, lats)
    map.plot(x, y, 'bo', markersize=6)

    for label, xpt, ypt in zip(labels, x, y):
        plt.text(xpt, ypt, label)

    x2, y2 = map(tlats, tlons)
    map.plot(x2, y2, 'bo', markersize=4, color='red')
    plt.draw()
    plt.show()
    print ("Drawn map")

def get_coords_by_name(name):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+name+'&key=AIzaSyCQFP_o6t6AYdZ5ZrzWpQ-Ym4G_vQKB7wM'
    url = url.replace(' ', '+')
    print url
    response = urllib.urlopen(url)
    data = response.read()
    data2 = json.loads(data)
    results = data2['results']
    result = results[0]
    lat = result['geometry']['location']['lat']
    lng = result['geometry']['location']['lng']
    return lat, lng


def get_name_from_latlng(lat, lng):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(lat)+','+str(lng)+'&key=AIzaSyCQFP_o6t6AYdZ5ZrzWpQ-Ym4G_vQKB7wM'

    url = url.replace(' ', '+')
    print url
    response = urllib.urlopen(url)
    data = response.read()
    data2 = json.loads(data)
    results = data2['results']
    addresses = []
    for addr in results:
        address = []
        add_com = addr['address_components']
        for component in add_com:
            address.append(component['short_name'])
        addresses.append(address)
    return addresses
