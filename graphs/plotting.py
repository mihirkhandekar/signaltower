from gmplot import gmplot

def google_plot(lats, lons, clats, clons, cclats = None, cclons = None, online=False, filename='map.html'):

    # Latitudes, longitudes, Center latitudes, Center longitudes
    gmap = gmplot.GoogleMapPlotter(18.5162511, 73.8352121, 13)

    gmap.scatter(lats, lons, 'blue', size=7, marker=False)
    if(clats != None and clons != None):
        gmap.scatter(clats, clons, 'orange', size=12, marker=False)
    if(cclats != None and cclons != None):
        gmap.scatter(clats, clons, 'maroon', size=7, marker=False)

    import webbrowser
    url = filename
    new = 2
    gmap.draw(url)
    print "Drew map"
    webbrowser.open(url, new=new)

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


