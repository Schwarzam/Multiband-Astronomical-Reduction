import numpy as np
from scipy.ndimage import percentile_filter

def BlockAverage(data, blockx=8, blocky=8):
    """
    Compute the block average of an input data array. 

    The BlockAverage function takes an input data array and computes a block-averaged array of the input data, where the block size is defined by blockx and blocky parameters. The output array is smaller than the input data because of the block averaging process. The function returns the block-averaged array of the input data.

    Parameters:
    -----------
    data: ndarray
        Input data array to be block averaged.
    blockx: int
        Size of the block in the x direction. Default is 8.
    blocky: int
        Size of the block in the y direction. Default is 8.

    Returns:
    --------
    ndarray
        A block-averaged array of the input data. The size of the output array is smaller than the input data
        because of the block averaging process.
    """
    sum_x = data[:-(blockx - 1):blockx, :]

    for nx in np.arange(1, blockx):
        sum_x = sum_x + data[nx::blockx, :]

    sum_y = sum_x[:, :-(blocky - 1):blocky]

    for ny in np.arange(1, blocky):
        sum_y = sum_y + sum_x[:, ny::blocky]

    blk_ave = sum_y / (blockx * blocky)
    return blk_ave

def percfilter(data, perc, size, blavgx=4, blavgy=4):
    """
    Applies a percentile filter to an input data array.

    The function applies a percentile filter to an input 2D data array, with the percentile value and filter size specified as parameters. An optional block average filter can also be applied before the percentile filter, with the size of the filter along the X and Y axes specified as parameters. The function returns the filtered data array.

    Parameters
    ----------
    data : numpy.ndarray
        Input 2D data array to be filtered.
    perc : float
        Percentile value to apply the filter.
    size : int or tuple of ints
        Size of the filter.
    blavgx : int, optional
        Size of the block average filter to apply to data along the X axis. Default is 4.
    blavgy : int, optional
        Size of the block average filter to apply to data along the Y axis. Default is 4.

    Returns
    -------
    numpy.ndarray
        The filtered data array.

    """
    if blavgx > 1:
        data = BlockAverage(data, blavgx, blavgy)

    data = percentile_filter(data, perc, size=size)
    return data
