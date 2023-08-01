from scipy import stats as scipyStats
import numpy as np

import mar

from mar.utilities.stats import MAD

def purge_outliers(x, n_sigma=3., n=5, med=False):
    for _ in range(n):
        medaux = np.median(x)
        if med:
            rms = MAD(x)
        else:
            rms = np.std(x)
        x = np.compress(np.less_equal(abs(x - medaux), n_sigma * rms), x)
    return x

def std_robust(x, n_sigma=3., n=5):
    x = purge_outliers(x, n_sigma, n, med=True)
    return np.std(x - np.mean(x, dtype='float64'), dtype='float64')

def arrStats(arr):
    """
    Computes various statistics for an input array.

    Args:
        arr (numpy array): The input array.

    Returns:
        tuple: A tuple containing the mode, median, mean, standard deviation, minimum, and maximum values of the input
            array.
    """
    median = np.median(arr)
    mean = arr.mean(dtype=np.float64)
    std = arr.std(dtype=np.float64)
    mini = arr.min()
    maxi = arr.max()
    mode = scipyStats.mode(np.round(arr,3), axis=None)[0][0]

    return mode, median, mean, std, mini, maxi 


def robustStat(arr, sigma=3, iters=5, med=False):
    """
    Computes various robust statistics for an input array.

    Args:
        arr (numpy array): The input array.
        sigma (float, optional): The number of standard deviations allowed for data to be considered as outlier.
            Defaults to 3.
        iters (int, optional): The number of iterations to perform the outlier rejection process. Defaults to 5.
        array. If not None, this overrides the `sigma` and `iters` parameters. Defaults to None.
        med (bool, optional): If True, use the median absolute deviation (MAD) instead of the standard deviation for
            outlier rejection. Defaults to False.

    Returns:
        dict: A dictionary containing the maximum, minimum, mean, median, standard deviation, fraction of rejected
            data points, robust standard deviation (nmad), and robust standard deviation (rms) of the input array.
    """
    arr = np.array(list(filter(lambda v: v==v, arr)))
    arr = arr[arr != np.array(None)]
    
    rms = None
    good = np.ones(len(arr), dtype=int)
    nx = sum(good)

    for i in range(len(arr)):
        if i > 0: xs = np.compress(good, arr)
        else: xs = arr
        aver = np.median(xs)
        if med: rms = mar.utilities.MAD(xs)
        else: rms = np.std(xs)
        good = good * np.less_equal(abs(arr - aver), sigma * rms)
        nnx = sum(good)
        if nnx == nx: break
        else: nx = nnx

    remaining = np.compress(good, arr)
    n_remaining = len(remaining)
    
    if n_remaining > 3:
        maxi = max(remaining)
        mini = min(remaining)
        mean = np.mean(remaining, dtype='float64')
        std = np.std(remaining, dtype='float64')
        median = np.median(remaining)
        auxl = float(len(remaining)) / 3.
        auxsort = remaining * 1.0
        auxsort.sort()

        fraction = 1. - (float(n_remaining) / float(len(arr)))
        nmad = mar.utilities.MAD(remaining)

    elif n_remaining > 1:
        maxi = max(remaining)
        mini = min(remaining)
        mean = np.mean(remaining, dtype='float64')
        std = np.std(remaining, dtype='float64')
        median = np.median(remaining)
        fraction = 1. - (float(n_remaining) / float(len(arr)))
        nmad = mar.utilities.MAD(remaining)
    elif n_remaining > 0:
        maxi = max(remaining)
        mini = min(remaining)
        mean = np.mean(remaining, dtype='float64')
        median = np.median(remaining)
        std = -1.0
        fraction = 1. - (float(n_remaining) / float(len(arr)))
        nmad = -99.99
    else:
        maxi = -1.0
        mini = 0.0
        mean = -1.0
        median = -1.0
        std = -1.0
        fraction = -1
        nmad = -99.99
    
    return {'maxi' :maxi, 'mini': mini, 'mean': mean, 'median': median, 'std':std, 'fraction': fraction, 'nmad':nmad, 'rms': rms}
