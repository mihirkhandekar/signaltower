import matplotlib.pyplot as plt
import numpy
import scipy.cluster.hierarchy as hcluster

from global_variables import clust_thresh


def cluster(data):
    N=100
    # clustering
    clusters = hcluster.fclusterdata(data, clust_thresh, criterion="distance")
    print "Cluster string " + str(clusters)
    # plotting
    plt.scatter(*numpy.transpose(data), c=clusters)
    plt.axis("equal")
    title = "threshold: %f, number of clusters: %d" % (clust_thresh, len(set(clusters)))
    plt.title(title)
    plt.show()