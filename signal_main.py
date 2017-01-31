from clustering.cluster import cluster
from functions.basicfunctions import get_all_signal_points_arrays, combine_separate_latlon
from functions.computationalfunctions import get_3_tuple
from functions.datafunctions import get_data, get_tower_locations
from graphs.plotting import google_plot
from trilateration.trilateration import trilaterate




def signal_main(provider, starttime, endtime, offline):
    lst, matrix, labels = get_data(provider, starttime, endtime, offline)

    # cnt = eliminate_outliers(matrix, labels)
    # print (str(cnt) + " points eliminated as outliers.")
    tuple3 = get_3_tuple(matrix, labels)
    print "Returned " + str(len(tuple3)) + " tuples"

    xcents, ycents, count = get_tower_locations(tuple3)
    print "Retrieved " + str(count) + " trilaterated towers"

    f1 = open("./trilat_towers.txt", "w+")
    f1.write(str(xcents) + "\n\n\n\n" +  str(ycents))
    print "Done writing to file"
    f1.close()

    # clust_matrix = combine_separate_latlon(xcents, ycents)



    # clust_centres = cluster(clust_matrix)


    xtows, ytows, labels = get_all_signal_points_arrays(matrix)

    # draw_chart(xcents, ycents)
    # show_on_map(xtows, ytows, labels, "", xcents, ycents)
    google_plot(xtows, ytows, xcents, ycents)
