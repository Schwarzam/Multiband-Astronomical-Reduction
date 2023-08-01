<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scienceimage.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reduction.scienceimage`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scienceimage.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `absoluteFilePaths`

```python
absoluteFilePaths(directory)
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scienceimage.py#L296"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `SuperFlatMask`

```python
SuperFlatMask(image=None, outdir='/tmp/')
```

Generates a mask for a science image. 



**Args:**
 
 - <b>`image`</b> (str):  The path to the science image. 
 - <b>`outdir`</b> (str):  The path to the output directory where the mask will be stored. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scienceimage.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PrepareSciImages`
A class to prepare science images for further processing. 



**Attributes:**
 
 - <b>`files`</b>:  a list of science files to be processed 
 - <b>`outdir`</b>:  output directory 
 - <b>`outputfiles`</b>:  boolean attribute indicating whether the output files will be saved 
 - <b>`outname`</b>:  output filename 
 - <b>`compress`</b>:  boolean attribute indicating whether the output fits files should be compressed 
 - <b>`shape`</b>:  the shape of the image 
 - <b>`gainPerAmp`</b>:  boolean attribute indicating whether the gain should be applied per amplifier 
 - <b>`bias`</b>:  bias image 
 - <b>`flat`</b>:  flat image 

Methods: 
 - <b>`__init__`</b> (self, folder=None, files = None, outdir='/tmp/', compress=False):  Constructor method. Initializes the class with the folder, files, output directory and compression options. 
 - <b>`run_overscan`</b> (self, masterBias=None, masterFlat=None, correct=True, gainPerAmp=False, subtract_bias=True, genThumb=False):  Runs overscan, bias subtraction and flat correction on the science images. 
 - <b>`overscan`</b> (self, file, subtract_bias, genThumb):  Performs overscan, bias subtraction and flat correction on a single science image. 
 - <b>`SuperFlat`</b> (self, files_to_fringe=None):  Creates a SuperFlat image. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scienceimage.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(folder=None, files=None, outdir='/tmp/', compress=False)
```

Initializes a new instance of the PrepareSciImages class. 



**Args:**
 
 - <b>`folder`</b> (str):  The path to the folder containing the science images. 
 - <b>`files`</b> (list):  A list of paths to the science images. 
 - <b>`outdir`</b> (str):  The path to the output directory where the prepared images will be stored. 
 - <b>`compress`</b> (bool):  Whether to compress the output images or not. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scienceimage.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `SuperFlat`

```python
SuperFlat(files_to_fringe=None)
```

Creates a super flat field from the science images. 



**Args:**
 
 - <b>`files_to_fringe`</b> (list):  A list of paths to the science images. 



**Returns:**
 The path to the super flat field. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scienceimage.py#L122"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `overscan`

```python
overscan(file, subtract_bias, genThumb)
```

Performs overscan, bias subtraction and flat correction on a single science image. 



**Args:**
 
 - <b>`file`</b> (str):  The path to the science image. 
 - <b>`subtract_bias`</b> (bool):  Whether to subtract the bias from the image. 
 - <b>`genThumb`</b> (bool):  Whether to generate a thumbnail image or not. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/scienceimage.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_overscan`

```python
run_overscan(
    masterBias=None,
    masterFlat=None,
    correct=True,
    gainPerAmp=False,
    subtract_bias=True,
    genThumb=False
)
```

Runs overscan, bias subtraction and flat correction on the science images in parallel. 



**Args:**
 
 - <b>`masterBias`</b> (str):  The path to the master bias frame. 
 - <b>`masterFlat`</b> (str):  The path to the master flat frame. 
 - <b>`correct`</b> (bool):  Whether to correct for the bias and flat or not. 
 - <b>`gainPerAmp`</b> (bool):  Whether to apply gain correction for each amplifier. 
 - <b>`subtract_bias`</b> (bool):  Whether to subtract the bias from the images. 
 - <b>`genThumb`</b> (bool):  Whether to generate a thumbnail image or not. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
