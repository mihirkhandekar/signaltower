import MySQLdb
import math
# from plotting import google_plot_freq_loc
import pprint
import urllib

"""
-Pick a radius for what you consider the size of a location (we'll say 100m)
-Iterate through your locations making them the center of your circle
-Count how many other points are within the circle using Point-in-Circle
-The location with the most points within it's circle becomes your most popular,
now remove all of those points from your set and repeat for 2nd most popular to nth most popular.
"""


class Location(object):
    def __init__(self):
        self.latitude = 0.000
        self.longitude = 0.000
        self.signal = 0

    def set_location(self,loc):
        self.latitude = loc[0]
        self.longitude = loc[1]
        self.signal = loc[2]

    def print_location(self):
        print str(self.latitude) + " " + str(self.longitude)


class Area(object):
    def __init__(self):
        self.centre = Location()
        self.location_set = []
        self.len = 0

    def set_Area(self,value, setloc, len):
        self.centre = value
        self.location_set.append(setloc)
        self.len = len


def measure(loc1, loc2):
    R = 6371  # Radius of earth in KM
    dLat = loc2.latitude * math.pi / 180 - loc1.latitude * math.pi / 180
    dLon = loc2.longitude * math.pi / 180 - loc1.longitude * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(loc1.latitude * math.pi / 180) * \
                                              math.cos(loc2.latitude * math.pi / 180) * \
                                              math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000  # meters


def find_set(loc, locations):
    radius = 500 #in m
    loc_set = [loc]
    for location in locations:
        if measure(loc, location) < 100:
            loc_set.append(location)
    return loc_set


def determine(loc1, loc2):
    if loc1.latitude != loc2.latitude:
        return 0
    if loc1.longitude == loc2.longitude:
        return 1


def get_freq(imei,top_n):
    '''
    db = MySQLdb.connect("projectdb1.czthhr2kqju8.us-east-1.rds.amazonaws.com", "mac", "mac113140", "sigdb")
    #db = MySQLdb.connect("localhost", "root", "root123", "testsignal")
    locations = []
    areas = []

    cursor = db.cursor()
    cursor.execute("select lat, lon, sig from sigtab where imei ='" + imei + "'")
    data = cursor.fetchall()

    for item in data:
        loc = Location()
        value = []
        lat = item[0]
        lon = item[1]
        sig = item[2]
        value.append(float(lat))
        value.append(float(lon))
        value.append(int(sig))
        loc.set_location(value)
        locations.append(loc)

    for location in locations:
        set_loc = find_set(location, locations)
        area = Area()
        area.set_Area(location, set_loc, len(set_loc))
        areas.append(area)
        for loc1 in set_loc:
            locations = [loc for loc in locations if not determine(loc,loc1)]
            #locations[:] = ifilterfalse(determine(loc1,locations), locations)

    desc_sort_set = sorted(areas, key=lambda area: area.len, reverse=True)
    if top_n < len(desc_sort_set):
        desc_sort_set = desc_sort_set[:top_n]

    lats1 =[]
    lons1 =[]
    lats2 = []
    lons2 = []
    lats3 = []
    lons3 = []

    # print "Top 1"
    # print str(desc_sort_set[0].len)
    for elem1 in desc_sort_set[0].location_set:
        for elem in elem1:
            lats1.append(elem.latitude)
            lons1.append(elem.longitude)
            #elem.print_location()

    # print "Top 2"
    # print str(desc_sort_set[1].len)
    for elem1 in desc_sort_set[1].location_set:
        for elem in elem1:
            lats2.append(elem.latitude)
            lons2.append(elem.longitude)
            #elem.print_location()
    # print "Top 3"
    # print str(desc_sort_set[2].len)

    for elem1 in desc_sort_set[2].location_set:
        for elem in elem1:
            lats3.append(elem.latitude)
            lons3.append(elem.longitude)
            #elem.print_location()
    db.close()

    # google_plot_freq_loc(lats1,lats2,lats3,lons1,lons2,lons3)
    lats = []
    lons = []
    for area in desc_sort_set:
        lats.append(area.centre.latitude)
        lons.append(area.centre.longitude)'''

    url = f'http://signalapps.herokuapp.com/frequentlocs?imei={str(imei)}&qty={str(top_n)}'

    response = urllib.urlopen(url)
    data = response.read()

    lats = []
    lons = []
    import ast
    data = data.replace("defaultdict(<type 'list'>, ", '')
    data = data.replace(')', '')
    data = ast.literal_eval(data)
    # print data
    for key, value in data.iteritems():
        # print key, value[0], value[1]
        lats.append(value[0])
        lons.append(value[1])

    return lats, lons

# pprint.pprint(get_freq('911438652523374', 4))