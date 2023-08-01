<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scan.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reduction.scan`






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scan.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Scan`
Class for overscan and prescan correction of an image 



**Args:**
 
 - <b>`filename`</b> (str, optional):  The name of the file to be corrected. Defaults to None. 
 - <b>`hdu`</b> (HDUList, optional):  The HDUList of the file to be corrected. Defaults to None. 
 - <b>`dmean`</b> (bool, optional):  Set to True to calculate the mean of the image. Defaults to False. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scan.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(filename=None, hdu=None, dmean=False)
```

hdu must be marfits HDUList instance (Opened with fromfile method). 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scan.py#L351"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `apply_subtraction`

```python
apply_subtraction(dataHDU, applytohdu=True)
```

Applies the overscan or prescan subtraction to the specified HDU data in-place, and returns the modified data. 



**Args:**
 
 - <b>`dataHDU`</b> (int):  The HDU index of the data to be corrected in the FITS file. 
 - <b>`applytohdu`</b> (bool):  Whether to modify the data in the HDU of the FITS file (default True). 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  The corrected data, after subtracting the calculated overscan or prescan value. 



**Raises:**
 
 - <b>`Exception`</b>:  If the shapes of the image and correction area do not match. 

The correction is performed by subtracting the calculated overscan or prescan value from the data within the image area, obtained from the data in the correction area previously defined by `calculate_offset()`. The method supports three types of fitting functions for the overscan/prescan correction: polynomial, spline, and median filter. The type of function used is specified by the `fitfunction` attribute of the Scan object. If the `applytohdu` parameter is set to True (default), the modified data is written back to the original HDU. The image area is defined by the `imsc_area` attribute of the Scan object, and correction areas are defined by `ovscx_area`, `ovscy_area`, `prscx_area`, `prscy_area`, and `direction` attributes. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scan.py#L123"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `calculate_offset`

```python
calculate_offset(direction, dataHDU)
```

Calculates the overscan or prescan offset values in the input image, depending on the value of the direction argument. This method is used internally by the run method to correct for overscan and prescan areas of the input image. 



**Args:**
 

self (object): the Scan object itself. direction (str): The direction to perform the calculation ('x' or 'y'). dataHDU (int): The index of the HDU in which the data is stored. 

**Returns:**
 

None The method calculates the overscan or prescan offset by first calculating the median or mean of the overscan or prescan areas of the input image. The method then interpolates over bad pixels and clips outliers to arrive at a corrected overscan or prescan offset. The method then saves the overscan or prescan offset values in the offset attribute of the Scan object, depending on the value of the direction argument. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scan.py#L484"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_areas`

```python
get_areas(amp, headerHDU)
```

Retrieves the values of the amplifiers inside header keywords from the HDU in order to identify and store the positions of  certain areas of interest within an image. 



**Parameters:**
 
----------- amp : int or str  The amplifier number or label. headerHDU : int  The index of the HDU containing the image header. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scan.py#L89"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(headerHDU=0, dataHDU=1, trim=True)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scan.py#L409"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `trim`

```python
trim(headerHDU, dataHDU, compress=False)
```

Trims a multi-output MAR CCD image and updates headers to reflect the trimmed size. 



**Args:**
 
 - <b>`headerHDU`</b> (int):  The index of the header HDU of the input data in the `Scan.hdu` attribute. 
 - <b>`dataHDU`</b> (int):  The index of the data HDU of the input data in the `Scan.hdu` attribute. 
 - <b>`compress`</b> (bool, optional):  Whether to compress the trimmed data array. Defaults to False. 



**Returns:**
 None 



**Raises:**
 None 

The method trims a multi-output MAR CCD image by extracting subarrays from the input data array defined by the sub-regions specified in the headers of the image. The method then updates the headers of the image to reflect the new trimmed size. The method takes as input the indices of the header and data HDUs in the `Scan.hdu` attribute. The `compress` argument can be set to True to compress the trimmed data array, but this functionality is currently commented out and has no effect. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
