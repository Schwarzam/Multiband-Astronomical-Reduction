<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `image.fits`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L499"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `getAmpArea`

```python
getAmpArea(amp)
```

Returns the image section of the given amplifier. 

Parameters 
---------- amp : int  The amplifier number. 

Returns 
------- list  The image section of the given amplifier. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MaskArray`
A class to handle masks within an array, extending numpy.ndarray. 

... 

Methods 
------- add_mask(mask : np.ndarray, value : int)  Add a mask with a certain value to the array. get_mask(values : List[int], binary : bool = False) -> np.ndarray  Get a mask from the array corresponding to certain values. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L44"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_mask`

```python
add_mask(mask, value)
```

Add a mask with a certain value to the array. 

Parameters 
---------- mask : np.ndarray  The mask to be added. Should be an array of 0s and 1s of the same shape as the MaskArray. value : int  The value to assign to the mask. Should be a power of 2 to allow bitwise operations. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_mask`

```python
get_mask(values, binary=False, inverted=False, dtype='uint8')
```

Get a mask from the array corresponding to certain values. 

Parameters 
---------- values : List[int]  A list of the mask values to include in the output mask. binary : bool, optional  If True, return a binary mask. If False (default), return a boolean mask. 

Returns 
------- result_mask : np.ndarray  The output mask. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `marfits`
A subclass of fits.HDUList with additional methods for handling MAR-specific FITS files. 



**Attributes:**
 
        - tabhdu: a reference to the TableHDU object associated with this FITS file. 
        - _file: the name of the file associated with this FITS file. 
        - hdus: a list of HDU objects associated with this FITS file. 
        - filename: the name of the file associated with this FITS file. 

Methods: 
        - __init__(self, hdus=[], file=None): initializes a new marfits object with optional hdus and file name parameters. 
        - fromfile(cls, file, mode="copyonwrite", memmap=False, **kwargs): returns a new marfits object by reading a FITS file. 
        - writeto(self, filename, compress=True, overwrite=False, usefilename=False): writes the contents of the marfits object to a new FITS file. 
        - writetosingle(self, filename, compress=True, overwrite=False, usefilename=False, headerhdu=0, datahdu=1): writes the contents of the marfits object to a new FITS file with only the specified header and data HDUs. 
        - updateheader(self, headerhdu=0, ignore_cards=[]): updates the header of the specified HDU with values from the MAR instrument configuration. 
        - transfheader(self, startext=0, endext=1): transfers the header cards from one HDU to another. 
        - setCard(self, card, value, comment='', headerhdu=0): sets a value for a specified card in the header of a specified HDU. 
        - delCard(self, card, headerhdu=0): removes a specified card from the header of a specified HDU. 
        - getCard(self, card, headerhdu=0): retrieves the value of a specified card from the header of a specified HDU. 
        - getAmpArea(self, amp): returns the pixel coordinates for a specified amplifier area. 

Usage:  Create a new marfits object from a FITS file: ``` fitsfile = marfits.fromfile('filename.fits')```

         Write the contents of a marfits object to a new FITS file:
         >>> fitsfile.writeto('newfilename.fits')

         Update the header of the second HDU in the FITS file with values from the MAR instrument configuration:
         >>> fitsfile.updateheader(headerhdu=1)

         Retrieve the value of the RA card from the header of the first HDU:
         >>> ra = fitsfile.getCard('RA')


<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L120"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(hdus=[], file=None)
```








---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L227"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_to_mask`

```python
add_to_mask(mask, value)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L435"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delCard`

```python
delCard(card, headerhdu=0)
```

Delete a specific header card in an HDU of the `marfits` object. 

Parameters 
---------- card : str  The name of the header card to delete. 

headerhdu : int, optional  The index of the HDU containing the header to delete the card from. Default is 0. 

Returns 
------- None 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L151"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `fromfile`

```python
fromfile(
    file,
    mode='copyonwrite',
    memmap=False,
    usemask=False,
    maskfile=None,
    **kwargs
)
```

Open a FITS file and return a `marfits` object with its HDUs. 

Parameters 
---------- file : str  The name of the FITS file to open. 

mode : str, optional  The mode to use for opening the file. The options are 'readonly',  'update', and 'copyonwrite'. Default is 'copyonwrite'. 

memmap : bool, optional  If True, use memory mapping to access the data in the file. Default is False. 

usemask : bool, optional  If True, loads `maskfile` FITS and append to `marfits`. Default is False. 

maskfile : str, optional  Mask filepath. Load mask FITS file and append to the `marfits`. Default is   None. 

**kwargs  Additional arguments to pass to the `fits.open` function. 

Returns 
------- hdus : `marfits`  A `marfits` object containing the HDUs of the FITS file. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L480"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getAmpArea`

```python
getAmpArea(amp)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L456"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getCard`

```python
getCard(card, headerhdu=0)
```

Get the value of a specific header card in an HDU of the `marfits` object. 

Parameters 
---------- card : str  The name of the header card to get the value of. 

headerhdu : int, optional  The index of the HDU containing the header to get the card value from. Default is 0. 

Returns 
------- object or bool  The value of the specified header card if it exists in the HDU header, else `False`. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L232"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_mask`

```python
get_mask(values=None, binary=False, inverted=False, dtype='uint8')
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L402"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `setCard`

```python
setCard(card, value, comment='', headerhdu=0)
```

Set the value of a specific header card in an HDU of the `marfits` object. 

Parameters 
---------- card : str  The name of the header card to set. 

value : object  The new value for the header card. 

comment : str, optional  A comment to add to the header card. Default is an empty string. 

headerhdu : int, optional  The index of the HDU containing the header to update. Default is 0. 

Returns 
------- None 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L376"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `transfheader`

```python
transfheader(startext=0, endext=1)
```

Transfer header information from one HDU to another in the `marfits` object. 

Parameters 
---------- startext : int, optional  The index of the source HDU to transfer header information from. Default is 0. 

endext : int, optional  The index of the destination HDU to transfer header information to. Default is 1. 

Returns 
------- None 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L331"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `updateheader`

```python
updateheader(headerhdu=0, ignore_cards=[])
```

Update the header of an HDU of the `marfits` object with instrument configuration. 

Parameters 
---------- headerhdu : int, optional  The index of the HDU containing the header to update. Default is 0. 

ignore_cards : list of str, optional  A list of header cards to ignore when updating the header. Default is an  empty list. 

Returns 
------- `marfits`  A new `marfits` object with the updated header. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L239"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_mask`

```python
write_mask(maskfile)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L244"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `writeto`

```python
writeto(filename, compress=True, overwrite=False, usefilename=False)
```

Write the HDUs of the `marfits` object to a FITS file. 

Parameters 
---------- filename : str  The name of the FITS file to write to. 

compress : bool, optional  If True, compress the output file using fpack. Default is True. 

overwrite : bool, optional  If True, overwrite any existing file with the same name. Default is False. 

usefilename : bool, optional  If True, use the `filename` attribute of the `marfits` object as the name  of the output file. Default is False. 

Returns 
------- None 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/fits.py#L286"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `writetosingle`

```python
writetosingle(
    filename,
    compress=True,
    overwrite=False,
    usefilename=False,
    headerhdu=0,
    datahdu=1
)
```

Write a single HDU of the `marfits` object to a FITS file. 

Parameters 
---------- filename : str  The name of the FITS file to write to. 

compress : bool, optional  If True, compress the output file using fpack. Default is True. 

overwrite : bool, optional  If True, overwrite any existing file with the same name. Default is False. 

usefilename : bool, optional  If True, use the `filename` attribute of the `marfits` object as the name  of the output file. Default is False. 

headerhdu : int, optional  The index of the HDU containing the header to write to the output file. Default is 0. 

datahdu : int, optional  The index of the HDU containing the data to write to the output file. Default is 1. 

Returns 
------- None 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
