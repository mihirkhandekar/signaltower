from signal_main import signal_main
import global_variables

from multiprocessing import Pool

if __name__ == "__main__":

    provider = "airtel"
    starttime = "2017-01-10+00%3A00%3A00"
    endtime = "2017-01-28+00%3A00%3A00"
    offline = False


    '''if __name__ == '__main__':
        pool = Pool(processes=1)  # Start a worker processes.
        result = pool.apply_async(signal_main, , callback)  # Evaluate "f(10)" asynchronously calling callback when finished.
    '''

    signal_main(provider, starttime, endtime, offline)

    global_variables.max_signal = -40

    global_variables.signal_factor = 1.2        # 0.7, 2.0, 0.1
    global_variables.division_factor = 1000     # 900, 1100, 2
    global_variables.max_range = 400            # 300, 700, 20

    ## Point selection variables
    # 50, 200 is optimal
    global_variables.tup_min_dist = 75          #
    global_variables.tup_max_dist = 170
    global_variables.outlier_check_dist = 10
    global_variables.outlier_pct = 20

