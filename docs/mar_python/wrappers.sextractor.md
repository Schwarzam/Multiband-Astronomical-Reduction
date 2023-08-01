<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/sextractor.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `wrappers.sextractor`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/sextractor.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `FilterSky`

```python
FilterSky(
    image,
    outfolder,
    BACK_FILTERSIZE=1,
    BACK_SIZE=21,
    DETECT_THRESH=1000,
    DETECT_MINAREA=10,
    ANALYSIS_THRESH=100,
    CHECKIMAGE_TYPE=None,
    CHECKIMAGE_NAME='im.fits',
    WEIGHT_IMAGE='weight.fits',
    CATALOG_NAME='out.cat'
)
```

Runs sextractor on an image to create a catalog, and save it to the specified output folder. 



**Args:**
 
- image (str): Path to the image file. 
- outfolder (str): Folder where the output files will be saved. 
- BACK_FILTERSIZE (int): Background filter size for sextractor. Default is 1. 
- BACK_SIZE (int): Background mesh size for sextractor. Default is 21. 
- DETECT_THRESH (float): Detection threshold for sextractor. Default is 1000. 
- DETECT_MINAREA (int): Minimum number of connected pixels for detection by sextractor. Default is 10. 
- ANALYSIS_THRESH (float): Threshold for analysis by sextractor. Default is 100. 
- CHECKIMAGE_TYPE (str or None): Type of the check image to be created by sextractor. If None, no check image will be created. Default is None. 
- CHECKIMAGE_NAME (str): Name of the check image file. Default is 'im.fits'. 
- WEIGHT_IMAGE (str): Name of the weight image file. Default is 'weight.fits'. 
- CATALOG_NAME (str): Name of the catalog file. Default is 'out.cat'. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/sextractor.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SExtr`
Class for running sextractor on an image. 



**Args:**
 
- image (str): Path to the image file. 
- addconf (dict): Dictionary containing additional configurations for sextractor. Default is None. 
- defaultconf (dict): Dictionary containing default configurations for sextractor. Default is None. 
- read_addconf (str): Path to an existing config file to be loaded as additional configurations. Default is None. 
- read_defaultconf (str): Path to an existing config file to be loaded as default configurations. Default is None. 
- folder (str): Folder where the output files will be saved. Default is '/tmp/'. 
- command (str): Path to the sextractor executable file. Default is 'sex'. 
- catname (str): Name of the output catalog file. Default is 'catout.param'. 



**Attributes:**
 
- config (dict): Dictionary containing the sextractor configuration. 
- params (list): List containing the names of the parameters to be extracted by sextractor. 

Methods: 
- run(): Runs sextractor with the current configuration and the specified image file. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/sextractor.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    image=None,
    addconf=None,
    defaultconf=None,
    read_addconf=None,
    read_defaultconf=None,
    folder='/tmp/',
    command='sex',
    catname='catout.param'
)
```








---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/sextractor.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run()
```

Runs sextractor with the current configuration and the specified image file.  






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
