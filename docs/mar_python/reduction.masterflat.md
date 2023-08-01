<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterflat.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reduction.masterflat`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterflat.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `absoluteFilePaths`

```python
absoluteFilePaths(directory)
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterflat.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MasterFlat`
Class to perform MasterFlat operations. 



**Attributes:**
 
 - <b>`outdir`</b> (str):  directory where all results will be saved. 
 - <b>`files`</b> (list):  list with all file paths. 
 - <b>`shape`</b> (tuple):  tuple with the dimensions of each element of files list. 
 - <b>`tmpfiles`</b> (list):  list with all temporary files. 
 - <b>`gainPerAmp`</b> (bool):  calculate GAIN per amp and run IRAF per amplifier (DEPRECATED). 
 - <b>`outfiles`</b> (list):  list with all output file paths. 
 - <b>`masterbias`</b> (str):  path to masterbias file. 
 - <b>`hdu`</b>:  instance of mar.image.marfits. 
 - <b>`bpmask`</b>:  instance of mar.image.marfits. 



**Args:**
 
 - <b>`folder`</b> (str, optional):  folder path to get all items in folder, usually not ideal. Defaults to None. 
 - <b>`files`</b> (list, optional):  list with all file paths, ideal way to input files. Defaults to None. 
 - <b>`outdir`</b> (str, optional):  directory where all results will be saved. Defaults to '/tmp/'. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterflat.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(folder=None, files=None, outdir='/tmp/')
```

Class to perform MasterFlat operations.  



**Args:**
 
 - <b>`folder`</b> (str, optional):  folder path to get all items in folder, usually not ideal. Defaults to None. 
 - <b>`files`</b> (list, optional):  list with all file paths, ideal way to input files. Defaults to None. 
 - <b>`outdir`</b> (str, optional):  directory where all results will be saved. Defaults to '/tmp/'. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterflat.py#L237"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `del_procfiles`

```python
del_procfiles()
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterflat.py#L223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getBPM`

```python
getBPM(filename=None)
```

Compute cold mask to incombined masterflat 



**Args:**
 
 - <b>`filename`</b> (str, optional):  masterflat file name. Defaults to None. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterflat.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `overscan`

```python
overscan(file, masterBias, subtract_bias, gainPerAmp, genThumb)
```

Run overscan on single file. 



**Args:**
 
 - <b>`file`</b> (_type_):  flat file to perform overscan 
 - <b>`masterBias`</b> (_type_):  masterBias path to perform subtraction of file. Defaults to None. 
 - <b>`subtract_bias`</b> (_type_):  perform BIAS subtraction, if true must give masterBias path. 
 - <b>`gainPerAmp`</b> (_type_):  calculate GAIN per amp and run IRAF per amplifier (DEPRECATED). 
 - <b>`genThumb`</b> (_type_):  Generate image of intermediates. Defaults to False. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterflat.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_imcombine`

```python
run_imcombine(delete_after=True, name=None)
```

Run iraf Imcombine on files loaded on class. They must be overscanned before.  



**Args:**
 
 - <b>`delete_after`</b> (bool, optional):  Delete tmp files after. Defaults to True. 
 - <b>`name`</b> (str, optional):  name to masterFlat file. Defaults to None. If None, name will be MasterFlat.fits 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterflat.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_overscan`

```python
run_overscan(
    masterBias=None,
    subtract_bias=True,
    gainPerAmp=False,
    genThumb=False
)
```

Run overscan on threads of files loaded to masterFlat class. 



**Args:**
 
 - <b>`masterBias`</b> (str, optional):  masterBias path to perform subtraction of file. Defaults to None. 
 - <b>`subtract_bias`</b> (bool, optional):  perform BIAS subtraction, if true must give masterBias path. Defaults to True. 
 - <b>`gainPerAmp`</b> (bool, optional):  calculate GAIN per amp and run IRAF per amplifier (DEPRECATED). Defaults to False. 
 - <b>`genThumb`</b> (bool, optional):  Generate image of intermediates. Defaults to False. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
