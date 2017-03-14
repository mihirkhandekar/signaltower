import math
import pprint
import urllib

import flask.json
import numpy
import random

import global_variables
import graphs.plotting


def gen_locations(loccount=10, bottomleft=(18.491947, 73.798019), topright=(18.558069, 73.908411)):
    bllat = bottomleft[0]
    bllon = bottomleft[1]
    trlat = topright[0]
    trlon = topright[1]
    digits = max(str(bllat)[::-1].find('.'), str(bllon)[::-1].find('.'), str(trlat)[::-1].find('.'), str(trlon)[::-1].find('.'))

    loclats = []
    loclons = []
    for i in range(loccount):
        loclats.append(float(float(random.randrange(bottomleft[0] * (10 ** digits), topright[0] * (10 ** digits))) / float(10 ** digits)))
        loclons.append(float(float(random.randrange(bottomleft[1] * (10 ** digits), topright[1] * (10 ** digits))) / float(10 ** digits)))

    # print str(loclats)
    # print str(loclons)
    return loclats, loclons


def gen_measurements(tlats, tlons, llats, llons):
    from basicfunctions import measure
    signal = []
    for i in range(0, min(len(llats), len(llons)), 1):
        mindist = numpy.inf
        for j in range(min(len(tlats), len(tlons))):
            dist = measure(tlats[j], tlons[j], llats[i], llons[i])
            if dist < mindist:
                mindist = dist
        if mindist < global_variables.max_range:
            signal.append(int((global_variables.max_signal - mindist / global_variables.signal_factor)))
        else:
            signal.append(numpy.inf)

    slen = len(signal)

    newlat = []
    newlon = []
    newsig = []

    for i in range(0, slen):
        if signal[i] != numpy.inf:
            newlat.append(llats[i])
            newlon.append(llons[i])
            newsig.append(signal[i])

    return newlat, newlon, newsig



def gen_routes(noofroutes=100):
    fname = 'generated_routes'
    import os, pickle
    if os.path.isfile(fname):
        os.chdir(r'/home/mihir/PycharmProjects/SignalTower/ml')
        routeslist = pickle.load(open(fname, 'rb'))
        return routeslist

    routeslist = []
    i = 0
    for route in range(noofroutes):
        routelist = []
        lats, lons = gen_locations(2)
        startlat = str(lats[0])
        startlon = str(lons[0])
        endlat = str(lats[1])
        endlon = str(lons[1])
        print str(i), startlat, startlon, 'to', endlat, endlon
        i += 1
        url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+ startlat+ ',' + startlon +'&destination='+ endlat+ ',' + endlon +'&key=AIzaSyCQFP_o6t6AYdZ5ZrzWpQ-Ym4G_vQKB7wM'
        print url
        response = urllib.urlopen(url)
        data = response.read()
        data2 = flask.json.loads(data)
        routes = data2['routes']
        route = routes[0]
        steps = route['legs'][0]['steps']
        seconds = 0.0
        routelist.append([float(startlat), float(startlon), seconds])
        for step in steps:
            steptime = step['duration']['text']
            timecomponents = steptime.split(' ')
            if 'min' in timecomponents[1]:
                stepsec = float(timecomponents[0]) * 60.0
            elif 'sec' in timecomponents[1]:
                stepsec = float(timecomponents[0])
            else:
                continue
            seconds += float(stepsec)
            curlat = step['end_location']['lat']
            curlon = step['end_location']['lng']
            routelist.append([curlat, curlon, seconds])
        routeslist.append(routelist)
        # pprint.pprint(routelist)

    # routedict = dict()
    # routedict['testimei'] = routeslist
    with open(fname, 'wb') as f:
        pickle.dump(routeslist, f)
        pass
    f.close()
    return routeslist


if __name__ == "__main__":
    '''nooftowers = 60
    reading_tower_ratio = 40
    tlats, tlons = gen_locations(nooftowers)
    llats, llons = gen_locations(nooftowers * reading_tower_ratio)
    llats, llons, signal = gen_measurements(tlats, tlons, llats, llons)
    print "signals", str(signal)
    graphs.plotting.google_plot(tlats, tlons, llats, llons, filename="randomtows.html")
    print max(signal), min(signal), len(signal)'''
    gen_routes(10)


    # print str(point_dist_angle(18.529313, 73.858176, 195, 200))
