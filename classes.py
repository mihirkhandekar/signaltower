class SignalPoint(object):
    def __init__(self):
        self.lat = 0.0
        self.lon = 0.0
        self.sig = 0.0

    def new_point(self, lat, lon, sig):
        self.lat = lat
        self.lon = lon
        self.sig = sig

    def print_point(self):
        print str(self.lat) + " " + str(self.lon) + " " + str(self.sig)

    def print_loc(self):
        print str(self.lat) + ", " + str(self.lon)


class Tuple3(object):
    def newTuple(self, sp1, sp2, sp3):
        self.sp1 = sp1
        self.sp2 = sp2
        self.sp3 = sp3
    def printTuple(self):
        self.sp1.print_loc()
        self.sp2.print_loc()
        self.sp3.print_loc()
