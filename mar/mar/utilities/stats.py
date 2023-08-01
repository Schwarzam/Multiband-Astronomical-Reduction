import numpy as np
from astropy.stats import mad_std, sigma_clip


def MAD(arr, axis=None):
    """
    Calculate the Median Absolute Deviation (MAD) of an array.

    Parameters:
    -----------
    arr : array-like
        Input data.

    Returns:
    --------
    res : array or float
        MAD of the input array.

    """

    res = mad_std(arr)
    return res


def interpolate(arr, sigma):
    """
    Interpolates outliers in the input array by replacing them with the
    interpolated values from the nearest non-outlier values.

    Parameters
    ----------
    arr : array_like
        The input array of values to be interpolated.
    sigma : float
        The number of standard deviations to use as the clipping limit
        when identifying outliers.

    Returns
    -------
    np.ndarray
        The interpolated array.

    """
    # Perform sigma clipping on the array
    d, l, upper = sigma_clip(arr, sigma=sigma, maxiters=1, cenfunc='median', stdfunc=MAD, return_bounds=True)
    
    # Find the elements in the array that are above the upper bound
    cutUp = arr > upper
    
    # Select the elements that are below the upper bound
    lower = arr[np.logical_not(cutUp)]
    
    # Interpolate the values above the upper bound using the values below the upper bound
    interpol = np.interp(cutUp.nonzero()[0], np.logical_not(cutUp).nonzero()[0], lower)
    
    # Replace the values above the upper bound with the interpolated values
    arr[cutUp] = interpol
    
    # Return the array with the interpolated values
    return arr


def median_robust(arr, axis=None, sigma=3, maxiters=1):
    """Calculate the median value of an array with robust estimation.

    The median is calculated using a robust estimator that iteratively sigma-clips the data to remove outliers.

    Args:
        arr (array-like): Input data.
        axis (int, tuple): Axis or axes along which to perform the operation. Default is None.
        sigma (float): The number of standard deviations to use for clipping. Default is 3.
        maxiters (int): The maximum number of iterations to perform. Default is 1.

    Returns:
        float or ndarray: The median of the input array.
    """
    arr = sigma_clip(arr, sigma=sigma, maxiters=maxiters, cenfunc='median', stdfunc=np.std, axis=axis, copy=True)
    res = np.ma.median(arr, axis=axis)
    return res


def mean_robust(arr, axis=None, sig=3, iters=2):
    """Calculate the mean value of an array with robust estimation.

    The mean is calculated using a robust estimator that iteratively sigma-clips the data to remove outliers.

    Args:
        arr (array-like): Input data.
        axis (int, tuple): Axis or axes along which to perform the operation. Default is None.
        sig (float): The number of standard deviations to use for clipping. Default is 3.
        iters (int): The maximum number of iterations to perform. Default is 2.

    Returns:
        float or ndarray: The mean of the input array.
    """
    arr = sigma_clip(arr, sigma=sig, maxiters=iters, cenfunc='mean', stdfunc=np.std, axis=axis, copy=True)
    res = np.ma.mean(arr, axis=axis, dtype='float')
    return res


def mean_robust2(arr, axis=None, sig=3, iters=1):
    """Calculate the mean value of an array with robust estimation.

    The mean is calculated using a robust estimator that iteratively sigma-clips the data to remove outliers.

    Args:
        arr (array-like): Input data.
        axis (int, tuple): Axis or axes along which to perform the operation. Default is None.
        sig (float): The number of standard deviations to use for clipping. Default is 3.
        iters (int): The maximum number of iterations to perform. Default is 1.

    Returns:
        float: The mean of the input array.
    """
    arr = sigma_clip(arr, sigma=sig, maxite=iters, cenfunc='median', stdfunc=MAD)
    res = np.mean(arr, dtype='float')
    return res


def purge_outliers(x, n_sigma=3., n=5, med=False):
    """
    Returns a filtered version of the input array x that removes any values more than n_sigma standard deviations away
    from the median, where the median and standard deviation are computed using the median absolute deviation (MAD).
    
    Args:
        x (numpy.ndarray): Input array to be filtered.
        n_sigma (float): Number of standard deviations away from the median to consider as an outlier.
        n (int): Number of iterations of outlier removal to perform.
        med (bool): If True, use the median of x instead of the mean to compute the MAD.
   
    Returns:
        numpy.ndarray: Filtered version of the input array x.
    """
    for _ in range(n):
        medaux = np.median(x)
        if med:
            rms = MAD(x)
        else:
            rms = np.std(x)
        x = np.compress(np.less_equal(abs(x - medaux), n_sigma * rms), x)
    return x


def std_robust(x, n_sigma=3., n=5):
    """
    Calculate the robust standard deviation of an array along a specified axis.

    Parameters:
    x (array_like): Input data.
    n_sigma (float, optional): The number of standard deviations to use as a threshold for outliers. Default is 3.
    n (int, optional): The number of iterations used to remove outliers. Default is 5.

    Returns:
    float or ndarray: The robust standard deviation of the input array.

    """
    x = purge_outliers(x, n_sigma, n, med=True)
    return np.std(x - np.mean(x, dtype='float64'), dtype='float64')