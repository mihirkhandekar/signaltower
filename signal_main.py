import time

import functions.computationalfunctions
from functions.basicfunctions import get_all_signal_points_arrays, combine_separate_latlon, arffFile
from functions.datafunctions import get_data, getCentres
from graphs.plotting import google_plot




def signal_main(provider, starttime, endtime, offline, getcentres=False, createFile=False, plot=False):
    start_time = time.time()
    lst, matrix, labels, cclat, cclon = get_data(provider, starttime, endtime, offline)
    print "Data Fetch Time elapsed: {:.2f}s".format(time.time() - start_time)

    start_time = time.time()

    xcents, ycents, count = functions.computationalfunctions.get_tower_locations(matrix, labels, lateration='tri')
    print "Retrieved " + str(count) + " trilaterated towers"
    print "Computation Time elapsed: {:.2f}s".format(time.time() - start_time)
    # cclat = None
    # cclon = None
    if(getcentres):
        cclat, cclon = getCentres(provider, starttime, endtime)

    if (createFile):
        arffFile(xcents, ycents, provider, starttime, endtime)
    if plot:
        xtows, ytows, labels = get_all_signal_points_arrays(matrix)
        google_plot(xtows, ytows, xcents, ycents, cclat, cclon)

