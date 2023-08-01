<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/Scamp.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `wrappers.Scamp`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/Scamp.py#L335"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `readScampHead`

```python
readScampHead(path)
```

Reads the header information from a SCAMP output file and returns a list of lists, where each sublist contains the name, value, and comment for a single header entry. 



**Args:**
 
 - <b>`path`</b> (str):  The path to the SCAMP output file to read. 



**Returns:**
 
 - <b>`list`</b>:  A list of lists, where each sublist contains the name, value, and comment for a single header entry. 



**Raises:**
 
 - <b>`FileNotFoundError`</b>:  If the specified file path does not exist. 



**Example:**
 ``` readScampHead('/path/to/my/file.fits.head')```
    [['SIMPLE', 'T', 'file conforms to FITS standard'],
      ['BITPIX', '-32', 'number of bits per data pixel'],
      ['NAXIS', '2', 'number of data axes'],
      ['NAXIS1', '1300', 'length of data axis 1'],
      ['NAXIS2', '1000', 'length of data axis 2'],
      ['EXTEND', 'T', 'FITS dataset may contain extensions'],
      ...
    ]



---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/Scamp.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Scamp`
A class for running Scamp 

Methods 
------- run()  Run Scamp. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/Scamp.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    catalog,
    c=None,
    verbose=5,
    tmpscmpfile=None,
    outdir='/tmp/',
    addconf=None,
    defaultconf=None,
    read_addconf=None,
    read_defaultconf=None
)
```

Scamp initialization. 

Parameters 
---------- catalog : str  Name of the catalog file. c : None, optional  Not used, by default None. verbose : int, optional  Level of verbosity of the outputs, by default 5. tmpscmpfile : None, optional  Not used, by default None. outdir : str, optional  Path to the output directory, by default '/tmp/'. addconf : None, optional  Additional configuration parameters, by default None. defaultconf : None, optional  Default configuration parameters, by default None. read_addconf : None, optional  Read configuration parameters from file, by default None. read_defaultconf : None, optional  Read default configuration parameters from file, by default None. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/Scamp.py#L244"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run()
```

Run Scamp. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/Scamp.py#L263"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RunAstro`
A class for running Scamp. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/Scamp.py#L268"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(catalog, outdir='/tmp', fwhm_seeing=1.26125)
```

RunAstro initialization. 

Parameters 
---------- catalog : str  Name of the catalog file. outdir : str, optional  Path to the output directory, by default '/tmp/'. fwhm_seeing: str, optional  Seeing FWHM. Default is 1.26125. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/Scamp.py#L244"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run()
```

Run Scamp. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
