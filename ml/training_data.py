import pprint

import datetime

import gmplot

import functions.basicfunctions
import functions.datafunctions
import functions.datagenerate
import ml.frequency

route_part_sec = 180

min_dist = 50

step = 60.0


def secdiff(dt1, dt2):
    return float((abs(dt2 - dt1)).total_seconds())


def getImeiTrainList(imei, imeilist):
    imeitrainlist = []
    for imeis in imeilist:
        if imei == imeis or str(imei) == str(imeis):
            imeitrainlist.append(1)
        else:
            imeitrainlist.append(0)
    return imeitrainlist


def get_routes():
    (trainingdata, imeilist) = (functions.datafunctions.get_train_data())
    # pprint.pprint(trainingdata)
    routesbyimei = dict()
    for key, value in trainingdata.items():
        imei = key
        matrix = value
        routeslist = []
        routelist = []
        if len(matrix) < 1:
            continue
        startindex = 0
        routelist.append([matrix[startindex][0], matrix[startindex][1], 0.0])
        dist = min_dist + 1
              #lat, lon, location
        for i in range(1, len(matrix) - 1):
            if i == startindex:
                routelist.append([matrix[startindex][0], matrix[startindex][1], 0.0])

            curtime = datetime.datetime.strptime(matrix[i][2], '%Y-%m-%d %H:%M:%S')
            if dist < min_dist:
                prevtime = oldtime
            else:
                prevtime = datetime.datetime.strptime((matrix[i - 1][2]), '%Y-%m-%d %H:%M:%S')

            secdif = secdiff(curtime, prevtime)
            # print datetime.datetime.strptime(matrix[i][2], '%Y-%m-%d %H:%M:%S'), datetime.datetime.strptime((matrix[i - 1][2]), '%Y-%m-%d %H:%M:%S'), secdif
            dist = functions.basicfunctions.measure(matrix[i][0], matrix[i][1], matrix[i - 1][0], matrix[i - 1][1])
            # print matrix[i][0], matrix[i][1], matrix[i - 1][0], matrix[i - 1][1], dist
            if secdif < route_part_sec and dist > min_dist:
                timedif = secdiff(datetime.datetime.strptime(matrix[i][2], '%Y-%m-%d %H:%M:%S'), datetime.datetime.strptime((matrix[startindex][2]), '%Y-%m-%d %H:%M:%S'))
                if i != startindex:
                    routelist.append([matrix[i][0], matrix[i][1], timedif])
            elif dist < min_dist:
                oldtime = prevtime
                continue
            else:
                routeslist.append(routelist)
                startindex = i + 1
                routelist = []
                # routelist.append([matrix[startindex][0], matrix[startindex][1], 0.0])

        refinedroutes = []
        for route in routeslist:

            totaldist = functions.basicfunctions.measure(route[0][0], route[0][1], route[len(route) - 1][0], route[len(route) - 1][1])
            # dist in m, 200 m

            totaltime = abs(route[0][2] - route[len(route) - 1][2])
            # time in s, 900 s = 15 min
            if totaltime == 0.0:
                totalspeed = 10000
            else:
                totalspeed = float(float(totaldist) / float(totaltime))
            # print 'ROUTE', route
            # print totaldist, totaltime, totalspeed

            if len(route) > 2 and totaltime > 900:# and 5 < totalspeed < 33:
                refinedroutes.append(route)
        # print 'refinedroutes', len(refinedroutes)

        routesbyimei[imei] = refinedroutes
    imei = u'99999999999999'
    routesbyimei[imei] = functions.datagenerate.gen_routes(170)
    imeilist.append(imei)
    return routesbyimei, imeilist


def getpopularlocs(imei):
    return ml.frequency.get_freq(imei, 4)
    pass


def route_by_sec(route):
    sec = 0.0
    routeslist = []
    prevpoint = None
    print 'Route length :', len(route)
    i = 0
    while(i < len(route)):
        # if imei == '99999999999999':
        #     print i, '----', str(sec), str(route[i])

        if route[i][2] == sec:
            # if imei == '99999999999999':
            #     print 'equal _ ADDED', str(sec), str([route[i][0], route[i][1]])
            routeslist.append([route[i][0], route[i][1]])
            sec += step
        elif route[i][2] > sec:
            secdiff = float(route[i][2] - route[i-1][2])
            perdiff = sec - route[i-1][2]

            ratio = float(float(perdiff) / float(secdiff))
            newlat = route[i-1][0] + ((route[i][0] - route[i-1][0]) * ratio)
            newlon = route[i-1][1] + ((route[i][1] - route[i-1][1]) * ratio)
            routeslist.append([newlat, newlon])
            # if imei == '99999999999999':
            #     print 'great _ ADDED', str(sec), str([newlat, newlon])
            sec += step
            i -= 1
        i += 1
        # prevpoint = route[i]
    '''for point in route:
        # print '---', str(point)
        if point[2] == sec:
            # print str(sec), str([point[0], point[1]])
            routeslist.append([point[0], point[1]])
            sec += step
        elif point[2] > sec:
            secdiff = float(point[2] - prevpoint[2])
            perdiff = sec - prevpoint[2]

            ratio = float(float(perdiff) / float(secdiff))
            newlat = prevpoint[0] + ((point[0] - prevpoint[0])*ratio)
            newlon = prevpoint[1] + ((point[1] - prevpoint[1])*ratio)
            routeslist.append([newlat, newlon])
            # print str(sec), str([newlat, newlon])
            sec += step
        prevpoint = point'''

    return routeslist



def routes_by_sec(value):
    routes = []
    i = 0
    for route in value:
        i += 1
        routebysec = route_by_sec(route)
        print str(i), '. Route (BS) length ::', len(routebysec)
        routes.append(routebysec)
    return routes


def get_training_data_sec(routesbyimei, imeilist, ngram):
    X = []
    y = []
    for key, value in routesbyimei.items():
        imei = key
        print '~IMEI', imei, 'ROUTES', len(value)
        routes = routes_by_sec(value)       # value has the matrix of that IMEI
        # if key is '868416020884739' or '9999999999':
        #     pprint.pprint(routes)

        # poplat, poplon = getpopularlocs(imei)
        imeitrainlist = getImeiTrainList(imei, imeilist)

        # print 'imeitrainlist', imeitrainlist


        lat = [0.0 for i in range(ngram)]
        lon = [0.0 for i in range(ngram)]
        # time = [None for i in range(ngram)]
        for route in routes:
            if len(route) >= ngram + 1:
                for i in range(len(route) - ngram):
                    xpoint = []
                    for j in range(ngram):
                        lat[j] = route[i + j][0]
                        lon[j] = route[i + j][1]
                        # time[j] = route[i + j][2]
                        xpoint.extend((lat[j],lon[j]))
                    # xpoint.extend(poplat)
                    # xpoint.extend(poplon)
                    xpoint.extend(imeitrainlist)
                    X.append(xpoint)


                    latf = route[i + ngram][0]
                    lonf = route[i + ngram][1]

                    ypoint = [latf, lonf]

                    y.append(ypoint)
    return X, y


def get_training_data(routesbyimei, ngram):
    X = []
    y = []
    for key, value in routesbyimei.items():
        imei = key
        routes = value

        poplat, poplon = getpopularlocs(imei)

        lat = [0.0 for i in range(ngram)]
        lon = [0.0 for i in range(ngram)]
        time = [None for i in range(ngram)]
        for route in routes:
            if len(route) >= ngram + 1:
                for i in range(len(route) - ngram):
                    xpoint = []
                    for j in range(ngram):
                        lat[j] = route[i + j][0]
                        lon[j] = route[i + j][1]
                        time[j] = route[i + j][2]
                        xpoint.extend((lat[j], lon[j], time[j]))

                    timef = route[i + 3][2]

                    xpoint.extend([timef])
                    xpoint.extend(poplat)
                    xpoint.extend(poplon)

                    X.append(xpoint)

                    latf = route[i + ngram][0]
                    lonf = route[i + ngram][1]

                    ypoint = [latf, lonf]

                    y.append(ypoint)
    return X, y

# get_training_data_sec(routesbyimei, ngram)

if __name__ == '__main__':
    # pprint.pprint(get_routes())
    routes = get_routes()


    pprint.pprint(routes)

    print 'sec data', (get_training_data_sec(routes, 5))

    # pathlon = -117.2974695, -117.2980671, -117.2984607, -117.2979182, -117.2974082, -117.2966604, -117.2977518, -117.2987498, -117.2981491, -117.297708, -117.2972804, -117.2965301, -117.2979485, -117.2975028, -117.2980506, -117.2982983, -117.2976609, -117.2970861, -117.2969908, -117.2981731, -117.2987695, -117.2981146, -117.2976909, -117.2969674, -117.2969299, -117.298394
    # pathlat = 33.27172039, 33.27197757, 33.27217535, 33.27225324, 33.27218351, 33.27233921, 33.27242614, 33.27248971, 33.27268346, 33.27265944, 33.27263664, 33.27279608, 33.27281652, 33.27194103, 33.27176546, 33.27224514, 33.27222714, 33.27208829, 33.27237357, 33.27243373, 33.27262189, 33.27268296, 33.27265933, 33.27262125, 33.27282274, 33.27283925
    pathlat = []
    pathlon = []
    aroute = routes['99999999999999'][2]
    for point in aroute:
        pathlat.append(point[0])
        pathlon.append(point[1])


    gmap = gmplot.GoogleMapPlotter(pathlat[0], pathlon[0], 18)
    gmap.plot(pathlat, pathlon, 'cornflowerblue', edge_width=5)
    gmap.draw('map.html')


