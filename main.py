from signal_main import signal_main
import global_variables

from multiprocessing import Pool

if __name__ == "__main__":

    provider = "airtel"
    starttime = "2017-02-01+00%3A00%3A00"
    endtime = "2017-03-03+23%3A00%3A00"
    offline = False


    '''if __name__ == '__main__':
        pool = Pool(processes=1)  # Start a worker processes.
        result = pool.apply_async(signal_main, , callback)  # Evaluate "f(10)" asynchronously calling callback when finished.
    '''

    signal_main(provider, starttime, endtime, offline, plot=True, createFile=True)
