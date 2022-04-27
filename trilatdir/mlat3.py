import numpy as np
import scipy.optimize as opt

#Returns the distance from a point to the list of spheres
def calc_distance(point):
    return np.power(np.sum(np.power(centers-point,2),axis=1),.5)-rad

#Latitude/longitude to carteisan
def geo2cart(lat,lon):
    lat=np.deg2rad(lat)
    lon=np.deg2rad(lon)
    return np.vstack(
        (
            earth_radius * np.cos(lat) * np.cos(lon),
            earth_radius * np.cos(lat) * np.sin(lon),
            earth_radius * np.sin(lat),
        )
    ).T

#Cartesian to lat/lon
def cart2geo(xyz):
    if xyz.ndim==1: xyz=xyz[None,:]
    lat=np.arcsin(xyz[:,2]/earth_radius)
    lon=np.arctan2(xyz[:,1],xyz[:,0])
    return np.rad2deg(lat),np.rad2deg(lon)

#Minimization function.
def minimize(point):
    dist= calc_distance(point)
    return np.linalg.norm(dist/rad)



def multi():
    global earth_radius
    earth_radius = 6378.137 #6378
    p = ((18.530143, 73.854764, 0.216), (18.530835, 73.856097, 0.160), (18.530637, 73.857547, 0.173), (18.530052, 73.858177, 0.230) ,(18.530052, 73.858177, 0.230), (18.530052, 73.858177, 0.230), (18.530052, 73.858177, 0.230), (18.530052, 73.858177, 0.230))

    # p4 = (50.43, 80.25, 1242.27)
    # p5 = (32.959575, 89.081064, 800)

    points = np.vstack(p)
    lat    = points[:,0]
    lon    = points[:,1]
    global rad
    rad    = points[:,2]
    global centers
    centers = geo2cart(lat,lon)

    out=[]
    for x in range(30):
        latrand=np.average(lat/rad)*np.random.rand(1)*np.sum(rad)
        lonrand=np.average(lon/rad)*np.random.rand(1)*np.sum(rad)
        start=geo2cart(latrand,lonrand)
        end_pos=opt.fmin_powell(minimize,start, full_output=False)
        out.append([cart2geo(end_pos),np.linalg.norm(end_pos-geo2cart(36.989,91464))])


    out = sorted(out, key=lambda x: x[1])
    print str(out)
    print out[0][0][0][0], ',',out[0][0][1][0],'Distance:',out[0][1]

multi()