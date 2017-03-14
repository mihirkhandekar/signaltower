# https://www.analyticsvidhya.com/blog/2015/08/common-machine-learning-algorithms/

import pickle
import pprint

import sklearn.ensemble
import sklearn.linear_model
import sklearn.model_selection
import sklearn.neural_network
from sklearn import tree, linear_model, svm

import functions.basicfunctions
import functions.datafunctions
import functions.datagenerate
import ml.training_data
from frequency import get_freq

'''def dt_to_epoch(dt):
    datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    return (datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S') - datetime.datetime(1970, 1, 1)).total_seconds()'''


def clf_predict(lats, lons, reqimei='99999999999999', ngram = 4):
    routesbyimei, imeilist = ml.training_data.get_routes()

    print 'IMEILIST', imeilist

    print 'ROUTESBYIMEI'
    fname = 'dtr.pickle'

    import os.path
    if os.path.isfile(fname):
        os.chdir(r'/home/mihir/PycharmProjects/SignalTower/ml')
        clf = pickle.load(open(fname, 'rb'))
    else:
        clf = tree.DecisionTreeRegressor()  #ok
        # clf = sklearn.neural_network.MLPClassifier() # does not work for data
        # clf = linear_model.Lasso(alpha = 0.1) #BAD!
        # clf = linear_model.LassoLars(alpha=.1) #No
        # clf = linear_model.BayesianRidge() #No
        # clf = sklearn.linear_model.SGDClassifier(loss="hinge", penalty="l2") #No
        # clf = sklearn.neural_network.MLPRegressor(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
        # clf = sklearn.neural_network.MLPRegressor(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
        # clf = sklearn.neural_network.MLPRegressor(activation='identity', solver='lbfgs',learning_rate='adaptive', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1, max_iter=400)

    # activation identity() logistic tanh relu()
    # solver lbfgs sgd adam
    # learning_rate constant invscaling adaptive

    X, y = (ml.training_data.get_training_data_sec(routesbyimei, imeilist, ngram))

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
        X, y, test_size=0.33)

    print 'X rows', len(X), 'y rows', len(y)

    clf = clf.fit(X_train, y_train)
    print 'score', clf.score(X_train, y_train)

    with open(fname,'wb') as f:
        pickle.dump(clf,f)
        pass
    f.close()

    predictlist = []
    j = 0
    # poplat, poplon = ml.training_data.getpopularlocs(reqimei)
    for i in range(len(lats)):
        predictlist.extend([lats[i], lons[i]])
        j += 1

    # predictlist.extend(str(99999999999999))
    # predictlist.extend([60 * j])
    # predictlist.extend(poplat)
    predictlist.extend(ml.training_data.getImeiTrainList(reqimei, imeilist))
    y_result = clf.predict(X_test)
    distlist = []
    ab100 = 0
    all = 0
    for i in range(len(X_test)):
        dist = functions.basicfunctions.measure(y_test[i][0], y_test[i][1], y_result[i][0], y_result[i][1])
        distlist.append(dist)
        if dist < 150:
            ab100 += 1
        all += 1
    print 'ratio > 150', float(float(ab100)/float(all))

    # print reduce(lambda x, y: x + y, distlist) / len(distlist)


    return clf.predict([predictlist])


if __name__ == '__main__':
    ngram = 4
    add = ['' for i in range(ngram)]
    # for i in range(ngram - 1):
        # add[i] = raw_input('Enter location ' + str(i))
    # add[0] = 'Nal Stop, Pune'
    # add[1] = 'Reshma Bhurji, Karve Road, Pune'
    '''add[0] = 'German Bakery, Law college Road, Pune'
    add[1] = 'Swatantra Theater Group, BMCC Road, Pune'
    add[2] = 'Hotel Hill View Ex, BMCC Road, Pune'
    add[3] = 'Joshi Wadewale, BMCC Road, Pune'
    '''
    '''add[0] = 'Chitale Bandhu, FC Road, Pune'
    add[1] = 'Darshan Restaurant, Prabhat Road, Pune'
    add[2] = 'Cafe Peterdonuts, Prabhat Road, Pune'
    add[3] = 'Kobe Sizzlers, Law College, Pune'
    '''
    add[0] = 'COEP, FC Road, Pune'
    add[1] = 'Darshan Restaurant, Prabhat Road, Pune'
    add[2] = 'Cafe Peterdonuts, Prabhat Road, Pune'
    add[3] = 'Kobe Sizzlers, Law College, Pune'

    lats = []
    lons = []
    for addr in add:
        lat, lon = functions.datafunctions.get_coords_by_name(addr)
        print lat, lon
        lats.append(lat)
        lons.append(lon)
    predicted = clf_predict(lats, lons, ngram=ngram)
    names = functions.datafunctions.get_name_from_latlng(predicted[0][0], predicted[0][1])
    printnames = ''
    for items in names:
        printnames += items[0] + ' / '

    print str(predicted), printnames