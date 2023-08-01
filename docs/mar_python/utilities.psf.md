<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/psf.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utilities.psf`




**Global Variables**
---------------
- **gaussian_sigma_to_fwhm**

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/psf.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `fit_bright_stars`

```python
fit_bright_stars(
    image,
    catalog,
    flux_col='FLUX_AUTO',
    fwhm_col='FWHM_IMAGE',
    saturation_threshold=0.9
)
```

Perform PSF fitting on bright, non-saturated stars in an image, using photutils.  This aims to be a simple way to get more precise coordinates for stars in an image. 

Parameters 
---------- image : 2D array_like  Input image data. catalog : astropy.table.Table  The input SExtractor catalog. flux_col : str, optional  Column name for flux values in the input catalog. Default is 'FLUX_AUTO'. fwhm_col : str, optional  Column name for FWHM values in the input catalog. Default is 'FWHM_IMAGE'. saturation_threshold : float, optional  The flux percentile above which stars are considered to be bright and not saturated.   Default is 0.9. 

Returns 
------- result : astropy.table.Table  Table of the PSF fitting results. The table includes the fitted x and y coordinates ('x_fit' and 'y_fit'),   which have been adjusted to correct for a 1-pixel offset. fit_info : dict  Information about the fitting process from the LevMarLSQFitter. 

Notes 
----- The function first selects bright, non-saturated stars from the catalog. It then sets up a BasicPSFPhotometry  object with a DAOGroup, an IntegratedGaussianPRF model, and a LevMarLSQFitter. It performs PSF fitting on  the selected stars and returns the results. 

Examples 
-------- ``` from astropy.io import fits```
``` from astropy.table import Table``` ``` image = fits.getdata('image.fits')```
``` catalog = Table.read('catalog.fits')``` ``` result, fit_info = fit_bright_stars(image, catalog)```





---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
