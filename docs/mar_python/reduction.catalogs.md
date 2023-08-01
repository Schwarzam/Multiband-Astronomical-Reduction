<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/catalogs.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reduction.catalogs`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/catalogs.py#L124"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_distributed_objects`

```python
get_distributed_objects(
    catalog,
    n_grid=None,
    objects_per_cell=None,
    margin=None
)
```

Selects a uniform distribution of objects from a SExtractor catalog grid. 

Parameters 
---------- catalog : astropy.table.Table  The input SExtractor catalog. n_grid : int, optional  The number of cells along each axis of the grid. The total number of cells is n_grid*n_grid.   Default is 10. objects_per_cell : int, optional  The maximum number of objects to select from each cell. The function will select this number   of objects from all cells, unless some cells have fewer than this number of objects but more   than the specified margin. Default is 1. margin : int, optional  The minimum number of objects that a cell must have in order to influence the total number of   objects selected from all cells. If a cell has fewer than this number of objects, the function   will still select objects_per_cell objects from all other cells. Default is 5. 

Returns 
------- distributed_objects : astropy.table.Table  A table of the selected objects. 

Notes 
----- The function selects objects based on their X_IMAGE and Y_IMAGE values. It divides the image into  a grid of cells, then selects a uniform number of objects from each cell. The number of objects  selected from each cell is the smaller of objects_per_cell and the number of objects in the cell  with the smallest number of objects (provided that number is greater than or equal to the margin).  The selected objects are those with the smallest MAGERR_AUTO values. 

Examples 
-------- ``` from astropy.table import Table```
``` import numpy as np``` ``` catalog = Table({'X_IMAGE': np.random.rand(100), 'Y_IMAGE': np.random.rand(100), 'MAGERR_AUTO': np.random.rand(100)})```
``` distributed_objects = get_distributed_objects(catalog, n_grid=5, objects_per_cell=2, margin=1)``` 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/catalogs.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SExtractorCatalog`
Class that runs Sextractor with some defined values in config.  The goal here is to run a simple catalog to detect objects and some parameters. 



**Args:**
 
 - <b>`SExtr`</b> (mar.wrappers.SExtr):  Sextractor wrapper. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/catalogs.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    image,
    mask=None,
    winparams=True,
    folder='/tmp',
    catname='catout.param'
)
```









---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/catalogs.py#L68"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CatalogOperation`




<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/catalogs.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(catalog)
```

Instantiate class with catalog path name.  



**Args:**
 
 - <b>`catalog`</b> (str):  file path. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/catalogs.py#L116"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `saveStarsCatalog`

```python
saveStarsCatalog(path, overwrite=True)
```

Function to save stars catalog. Used to give to scamp.   



---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/catalogs.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `stars`

```python
stars(distributed=False)
```

Function to calculate inicial seeing FWHM, and some stats from given catalog.   






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
