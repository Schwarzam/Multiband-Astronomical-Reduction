<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/fringe.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reduction.fringe`






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/fringe.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FringeSubtract`
Class that performs the subtraction of fringes (interference patterns) in astronomical images. 

Methods: 
-------- __init__(self, superFlat):  Constructor method that reads the super-flat file, computes statistics, updates the header and sets the  HDU and number of output detectors. subtractMode(self, individualAmps=False):  Method that creates the fringe subtraction, subtracting the mode of the fringe from the image. ComputeContrast(self, hdu=None, headerHDU=0, dataHDU=0):  Method that computes the fringe contrast using Block Average and percentile filtering. ComputeBackgroundfactor(self, im, imdataHDU=1, outim='/tmp/im.fits'):  Method that subtracts the fringe contrast from the image. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/fringe.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(superFlat)
```

Constructor method that reads the super-flat file, computes statistics, updates the header and sets the HDU and number of output detectors. 



**Parameters:**
 
----------- superFlat : str  The filename of the super-flat file. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/fringe.py#L74"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ComputeBackgroundfactor`

```python
ComputeBackgroundfactor(im, imdataHDU=1, outim='/tmp/im.fits')
```

Method that subtracts the fringe contrast from the image. 



**Parameters:**
 
----------- im : str  The filename of the image to be corrected. imdataHDU : int, optional  The HDU containing the data. The default is 1. outim : str, optional  The filename of the corrected image. The default is '/tmp/im.fits'. 



**Returns:**
 
-------- None 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/fringe.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `subtractMode`

```python
subtractMode(individualAmps=False)
```

Method that creates the fringe subtraction, subtracting the mode of the fringe from the image. 



**Parameters:**
 
----------- individualAmps : bool, optional  If True, subtract the mode of the fringe for each amplifier separately. If False (default),  subtract the mean mode of the fringe for all amplifiers. 



**Returns:**
 
-------- None 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
