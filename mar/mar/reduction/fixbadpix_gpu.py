import numpy as np
from numba import jit, cuda

def py_apply_mask_gpu(indat, pixelmask, inmask=None, cleantype='idw',
                  set_background_value=False):
    # Grab the sizes of the input array
    nx = indat.shape[1]
    ny = indat.shape[0]

    # Set the initial values to those of the data array
    cleanarr = indat.copy()
    pixmask = pixelmask.copy()

    # Setup the mask
    if inmask is None:
        # By default don't mask anything
        mask = np.zeros((ny, nx), dtype=np.uint8, order='C')
    else:
        # Make a copy of the input mask
        mask = inmask.copy()

    # Masked mean filter
    if cleantype == 'meanmask':
        py_clean_meanmask_gpu(cleanarr, pixmask, mask, nx, ny)
    # Masked median filter
    elif cleantype == 'medmask':
        py_clean_medmask_gpu(cleanarr, pixmask, mask, nx, ny)
    # Inverse distance weighted interpolation
    elif cleantype == 'idw':
        py_clean_idwinterpolate_gpu(cleanarr, pixmask, mask, nx, ny)
    else:
        raise ValueError("""cleantype must be one of the following values:
                        [median, meanmask, medmask, idw]""")

    return cleanarr

@jit(target_backend='cuda')
def py_clean_idwinterpolate_gpu(cleanarr, crmask, mask, nx, ny):
    """clean_idwinterpolate(cleanarr, crmask, mask, nx, ny)\n
    Clean the bad pixels in cleanarr using a 5x5 using inverse distance
    weighted interpolation.

    Parameters
    ----------
    cleanarr : float numpy array
        The array to be cleaned.

    crmask : boolean numpy array
        Cosmic ray mask. Pixels with a value of True in this mask will be
        cleaned.

    mask : boolean numpy array
        Bad pixel mask. Values of True indicate bad pixels.

    nx : int
        Size of cleanarr in the x-direction (int). Note cleanarr has dimensions
        ny x nx.

    ny : int
        Size of cleanarr in the y-direction (int). Note cleanarr has dimensions
        ny x nx.

    """
    # Go through all of the pixels, ignore the borders
    weights = np.array([[0.35355339, 0.4472136, 0.5, 0.4472136, 0.35355339],
                        [0.4472136, 0.70710678, 1., 0.70710678, 0.4472136],
                        [0.5, 1., 0., 1., 0.5],
                        [0.4472136, 0.70710678, 1., 0.70710678, 0.4472136],
                        [0.35355339, 0.4472136, 0.5, 0.4472136, 0.35355339]],
                       dtype=np.float32)

    # For each pixel
    for j in range(2, ny - 2):
        for i in range(2, nx - 2):
            # if the pixel is in the crmask
            if crmask[j, i]:
                wsum = 0.0
                val = 0.0
                for l in range(-2, 3):
                    y = j + l
                    for k in range(-2, 3):
                        x = i + k
                        if not (crmask[y, x] or mask[y, x]):
                            y1 = l + 2
                            x1 = k + 2
                            val = val + weights[y1, x1] * cleanarr[y, x]
                            wsum = wsum + weights[y1, x1]
                if wsum >= 1e-6:
                    cleanarr[j, i] = val / wsum

@jit(target_backend='cuda')
def py_clean_meanmask_gpu(cleanarr, pixmask, mask, nx, ny):
    """ clean_meanmask(cleanarr, pixmask, mask, nx, ny)\n
    Clean the bad pixels in cleanarr using a 5x5 masked mean filter.

    Parameters
    ----------
    cleanarr : float numpy array
        The array to be cleaned.

    pixmask : boolean numpy array
        Pixels with a value of True in this mask will be cleaned.

    mask : boolean numpy array
        Bad pixel mask. Values of True indicate bad pixels.

    nx : int
        Size of cleanarr in the x-direction. Note cleanarr has dimensions
        ny x nx.

    ny : int
        Size of cleanarr in the y-direction. Note cleanarr has dimensions
        ny x nx.

    """
    # For each pixel
    for j in range(2, ny - 2):
        for i in range(2, nx - 2):
            # if the pixel is in the pixmask
            if pixmask[j, i]:
                numpix = 0
                s = 0.0

                # sum the 25 pixels around the pixel
                # ignoring any pixels that are masked
                for l in range(-2, 3):
                    for k in range(-2, 3):
                        badpix = pixmask[j + l, i + k]
                        badpix = badpix or mask[j + l, i + k]
                        if not badpix:
                            s = s + cleanarr[j + l, i + k]
                            numpix = numpix + 1

                # if the pixels count is 0
                # then put in the background of the image
                if numpix != 0:
                    s = s / float(numpix)
                    cleanarr[j, i] = s

@jit(target_backend='cuda')
def py_clean_medmask_gpu(cleanarr, pixmask, mask, nx, ny):
    """ clean_medmask(cleanarr, pixmask, mask, nx, ny)\n
    Clean the bad pixels in cleanarr using a 5x5 masked median filter.

    Parameters
    ----------
    cleanarr : float numpy array
        The array to be cleaned.

    pixmask : boolean numpy array
        Pixels with a value of True in this mask will be cleaned.

    mask : boolean numpy array
        Bad pixel mask. Values of True indicate bad pixels.

    nx : int
        size of cleanarr in the x-direction. Note cleanarr has dimensions
        ny x nx.

    ny : int
        size of cleanarr in the y-direction. Note cleanarr has dimensions
        ny x nx.

    """
    medarr = np.zeros((25), dtype=np.float32, order='C')
    for j in range(2, ny - 2):
        for i in range(2, nx - 2):
            # if the pixel is in the pixmask
            if pixmask[j, i]:
                numpix = 0
                # median the 25 pixels around the pixel ignoring
                # any pixels that are masked
                for l in range(-2, 3):
                    for k in range(-2, 3):
                        badpixel = pixmask[j + l, i + k]
                        badpixel = badpixel or mask[j + l, i + k]
                        if not badpixel:
                            medarr[numpix] = cleanarr[j + l, i + k]
                            numpix = numpix + 1

                # if the pixels count is 0 then put in the background
                # of the image
                if numpix != 0:
                    cleanarr[j, i] = np.median(medarr[0:numpix])
