import numpy as np
from astropy.io import ascii
from astropy.table import Table
from photutils.psf import DAOGroup, IntegratedGaussianPRF
from photutils.psf import BasicPSFPhotometry
from astropy.modeling.fitting import LevMarLSQFitter
from astropy.stats import gaussian_sigma_to_fwhm

def fit_bright_stars(image, catalog, flux_col='FLUX_AUTO', fwhm_col='FWHM_IMAGE', saturation_threshold=0.9):
    """
    Perform PSF fitting on bright, non-saturated stars in an image, using photutils. 
    This aims to be a simple way to get more precise coordinates for stars in an image.

    Parameters
    ----------
    image : 2D array_like
        Input image data.
    catalog : astropy.table.Table
        The input SExtractor catalog.
    flux_col : str, optional
        Column name for flux values in the input catalog. Default is 'FLUX_AUTO'.
    fwhm_col : str, optional
        Column name for FWHM values in the input catalog. Default is 'FWHM_IMAGE'.
    saturation_threshold : float, optional
        The flux percentile above which stars are considered to be bright and not saturated. 
        Default is 0.9.

    Returns
    -------
    result : astropy.table.Table
        Table of the PSF fitting results. The table includes the fitted x and y coordinates ('x_fit' and 'y_fit'), 
        which have been adjusted to correct for a 1-pixel offset.
    fit_info : dict
        Information about the fitting process from the LevMarLSQFitter.

    Notes
    -----
    The function first selects bright, non-saturated stars from the catalog. It then sets up a BasicPSFPhotometry 
    object with a DAOGroup, an IntegratedGaussianPRF model, and a LevMarLSQFitter. It performs PSF fitting on 
    the selected stars and returns the results.

    Examples
    --------
    >>> from astropy.io import fits
    >>> from astropy.table import Table
    >>> image = fits.getdata('image.fits')
    >>> catalog = Table.read('catalog.fits')
    >>> result, fit_info = fit_bright_stars(image, catalog)
    """
    # Function body goes here

    # Filter the catalog to select only the brighter and better stars (not saturated)
    # You can adjust the conditions based on your specific requirements
    bright_stars = catalog[(catalog[flux_col] > np.percentile(catalog[flux_col], saturation_threshold)) &
                           (catalog[fwhm_col] > 0)]
    
    bright_stars['x_0'] = bright_stars['XWIN_IMAGE']
    bright_stars['y_0'] = bright_stars['YWIN_IMAGE']
    
    # Set up the photometry and group objects
    daogroup = DAOGroup(2.0 * gaussian_sigma_to_fwhm)  # You can adjust the threshold based on your requirements
    fitter = LevMarLSQFitter()
    psf_model = IntegratedGaussianPRF(sigma=bright_stars[fwhm_col].mean() / gaussian_sigma_to_fwhm)

    # Perform the fit using BasicPSFPhotometry
    photometry = BasicPSFPhotometry(group_maker=daogroup, bkg_estimator=None,
                                    psf_model=psf_model, fitter=fitter,
                                    fitshape=(11, 11))  # You can adjust the fitshape based on your requirements
    result = photometry(image=image, init_guesses=Table(bright_stars))

    ### TODO: THIS HERE SHOULD BE REVISED ### 
    """
    In Python, as well as in Astropy, the pixel index is 0-based, 
    which means that the first pixel of an image has the coordinates (0, 0). 
    On the other hand, SExtractor uses a 1-based indexing, 
    which means that the first pixel has the coordinates (1, 1).
    """
    result["x_fit"] = result["x_fit"] + 1
    result["y_fit"] = result["y_fit"] + 1
    
    return result, fitter.fit_info
