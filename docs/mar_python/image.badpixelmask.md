<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/badpixelmask.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `image.badpixelmask`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/badpixelmask.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `computeHotMask`

```python
computeHotMask(data, sigma=5, maxiters=7)
```

Compute a hot pixel mask using sigma clipping. 

Parameters 
---------- data : array_like  The data to be masked. 

sigma : float, optional  The number of standard deviations to use for sigma clipping. Default is 5. 

maxiters : int, optional  The maximum number of iterations to use for sigma clipping. Default is 7. 

Returns 
------- mask : ndarray  A boolean array with the same shape as `data`, where True indicates a hot pixel. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/badpixelmask.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `computeColdMask`

```python
computeColdMask(filename, outfolder='/tmp', lowthres=0.96, highthres=1.04)
```

Compute a cold pixel mask using a master flat and background estimation. 

Parameters 
---------- filename : str  The name of the master flat file. 

outfolder : str, optional  The folder to write the background image to. Default is "/tmp". 

lowthres : float, optional  The lower threshold for the ratio of the master flat to the background. Default is 0.96. 

highthres : float, optional  The upper threshold for the ratio of the master flat to the background. Default is 1.04. 

Returns 
------- mask : ndarray  A boolean array with the same shape as the master flat, where True indicates a cold pixel. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
