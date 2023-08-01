import os
import warnings
import cv2

import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clip

import mar
from mar.config import MarManager
from mar.wrappers.sextractor import FilterSky


warnings.filterwarnings("ignore", message="Keyword name")


def computeHotMask(data, sigma=5, maxiters=7):
    """
    Compute a hot pixel mask using sigma clipping.

    Parameters
    ----------
    data : array_like
        The data to be masked.

    sigma : float, optional
        The number of standard deviations to use for sigma clipping. Default is 5.

    maxiters : int, optional
        The maximum number of iterations to use for sigma clipping. Default is 7.

    Returns
    -------
    mask : ndarray
        A boolean array with the same shape as `data`, where True indicates a hot pixel.

    """
    MarManager.INFO("Computing hotmask.")
    if not isinstance(data, np.ndarray):
        MarManager.WARN('Mask Computation input not right. Needs to be np.ndarray')
        return np.zeros_like(data, dtype=np.uint8)

    data = np.asarray(data, dtype=np.float64)

    # Apply sigma clipping to the data
    clip = sigma_clip(data, sigma=sigma, maxiters=maxiters, return_bounds=True)

    # Create a mask for NaNs and values outside the range of the clipped data
    mask = np.isnan(data) | np.isneginf(data) | np.isposinf(data) | (data > clip[2])

    return np.asarray(mask, dtype=np.uint8)


def computeColdMask(filename, outfolder="/tmp", lowthres=0.96, highthres=1.04):
    """
    Compute a cold pixel mask using a master flat and background estimation.

    Parameters
    ----------
    filename : str
        The name of the master flat file.

    outfolder : str, optional
        The folder to write the background image to. Default is "/tmp".

    lowthres : float, optional
        The lower threshold for the ratio of the master flat to the background. Default is 0.96.

    highthres : float, optional
        The upper threshold for the ratio of the master flat to the background. Default is 1.04.

    Returns
    -------
    mask : ndarray
        A boolean array with the same shape as the master flat, where True indicates a cold pixel.

    """
    MarManager.INFO("Computing coldmask.")

    # Load the master flat and estimate the background
    masterflat = fits.getdata(filename)
    FilterSky(filename, outfolder, CHECKIMAGE_TYPE='BACKGROUND')
    backdata = fits.getdata(os.path.join(outfolder, 'im.fits'))

    # Compute the ratio of the master flat to the background and create a mask for NaNs and values outside the range
    normf = masterflat / backdata
    mask = np.isnan(masterflat) | (normf < lowthres) | (normf > highthres)

    return np.asarray(mask, dtype=np.uint8)