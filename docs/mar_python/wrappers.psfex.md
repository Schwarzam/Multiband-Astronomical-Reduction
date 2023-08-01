<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/psfex.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `wrappers.psfex`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/psfex.py#L174"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `createVignetCatalog`

```python
createVignetCatalog(image, output)
```

Creates a catalog of vignettes (small cutouts) of stars in the given image using sextractor. 

:param image: path to the input image file :type image: str :param output: path to the output catalog file :type output: str 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/psfex.py#L239"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `filterCatalogToPSFex`

```python
filterCatalogToPSFex(tablepath)
```

Filters the given sextractor catalog file to keep only objects that are likely to be good PSF candidates. 

:param tablepath: path to the input catalog file :type tablepath: str 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/psfex.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PSFex`
A class for running PSFex, which models point spread functions (PSFs) of astronomical images based on selected point sources. 



**Args:**
 
 - <b>`catalog`</b> (str):  Input catalog to extract PSF model. 
 - <b>`command`</b> (str):  Command to run PSFex. 
 - <b>`folder`</b> (str):  Folder to store output files. 



**Attributes:**
 
 - <b>`command`</b> (str):  Command to run PSFex. 
 - <b>`catalog`</b> (str):  Input catalog to extract PSF model. 
 - <b>`folder`</b> (str):  Folder to store output files. 
 - <b>`config`</b> (dict):  Configuration dictionary. 

Methods: 
 - <b>`run`</b> ():  Runs PSFex on the catalog to extract PSF model. 
 - <b>`getPSFinfo`</b> ():  Extracts PSF model parameters from XML output. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/psfex.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(catalog=None, command='psfex', folder='./outputs/')
```

Initialize a PSFex object. 



**Args:**
 
 - <b>`catalog`</b> (str):  Input catalog to extract PSF model. 
 - <b>`command`</b> (str):  Command to run PSFex. 
 - <b>`folder`</b> (str):  Folder to store output files. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/psfex.py#L141"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getPSFinfo`

```python
getPSFinfo()
```

Parses the XML output of PSFex and returns a dictionary of relevant information. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/psfex.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run()
```

Runs PSFex with the configured options. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
