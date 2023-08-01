<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/fixbadpix.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reduction.fixbadpix`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/fixbadpix.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `py_apply_mask`

```python
py_apply_mask(
    indat,
    pixelmask,
    inmask=None,
    cleantype='idw',
    set_background_value=False
)
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/fixbadpix.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `py_clean_idwinterpolate`

```python
py_clean_idwinterpolate(cleanarr, crmask, mask, nx, ny)
```

clean_idwinterpolate(cleanarr, crmask, mask, nx, ny) 

Clean the bad pixels in cleanarr using a 5x5 using inverse distance weighted interpolation. 

Parameters 
---------- cleanarr : float numpy array  The array to be cleaned. 

crmask : boolean numpy array  Cosmic ray mask. Pixels with a value of True in this mask will be  cleaned. 

mask : boolean numpy array  Bad pixel mask. Values of True indicate bad pixels. 

nx : int  Size of cleanarr in the x-direction (int). Note cleanarr has dimensions  ny x nx. 

ny : int  Size of cleanarr in the y-direction (int). Note cleanarr has dimensions  ny x nx. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/fixbadpix.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `py_clean_meanmask`

```python
py_clean_meanmask(cleanarr, pixmask, mask, nx, ny)
```

clean_meanmask(cleanarr, pixmask, mask, nx, ny) 

Clean the bad pixels in cleanarr using a 5x5 masked mean filter. 

Parameters 
---------- cleanarr : float numpy array  The array to be cleaned. 

pixmask : boolean numpy array  Pixels with a value of True in this mask will be cleaned. 

mask : boolean numpy array  Bad pixel mask. Values of True indicate bad pixels. 

nx : int  Size of cleanarr in the x-direction. Note cleanarr has dimensions  ny x nx. 

ny : int  Size of cleanarr in the y-direction. Note cleanarr has dimensions  ny x nx. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/fixbadpix.py#L142"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `py_clean_medmask`

```python
py_clean_medmask(cleanarr, pixmask, mask, nx, ny)
```

clean_medmask(cleanarr, pixmask, mask, nx, ny) 

Clean the bad pixels in cleanarr using a 5x5 masked median filter. 

Parameters 
---------- cleanarr : float numpy array  The array to be cleaned. 

pixmask : boolean numpy array  Pixels with a value of True in this mask will be cleaned. 

mask : boolean numpy array  Bad pixel mask. Values of True indicate bad pixels. 

nx : int  size of cleanarr in the x-direction. Note cleanarr has dimensions  ny x nx. 

ny : int  size of cleanarr in the y-direction. Note cleanarr has dimensions  ny x nx. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
