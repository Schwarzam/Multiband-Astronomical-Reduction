<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterbias.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reduction.masterbias`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterbias.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `absoluteFilePaths`

```python
absoluteFilePaths(directory)
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterbias.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MasterBias`
Class to perform MasterBias operations. 



**Attributes:**
 
 - <b>`outdir`</b> (str):  directory where all results will be saved 
 - <b>`perAmp`</b> (bool):  run iraf per amplifier 
 - <b>`amps`</b> (int):  number of amplifiers 
 - <b>`ampSize`</b> (tuple):  size of the amplifier region 
 - <b>`orders`</b> (numpy.array):  amplifier orders 
 - <b>`indices`</b> (numpy.array):  amplifier indices 
 - <b>`files`</b> (list):  list with all file paths 
 - <b>`shape`</b> (tuple):  shape of the image 
 - <b>`tmpfiles`</b> (list):  list with intermediate file paths 

Methods: __init__(self, folder=None, files=None, outdir='/tmp/', perAmp=False):  Initializes the MasterBias class. 

run_overscan(self, genThumb=False):  Run overscan on files loaded to MasterBias Class. 

overscan(self, file, genThumb):  Run overscan routine. 

run_imcombine(self, delete_after=True):  Run iraf IMCOMBINE on files loaded on class.  These files must be overscanned before running IRAF. 

getBPM(self):  Generates Bad Pixel Mask (hotmask) for incombined result. 

del_procfiles(self):  Delete intermediate files. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterbias.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(folder=None, files=None, outdir='/tmp/', perAmp=False)
```

Class to perform MasterBias operations.  



**Args:**
 
 - <b>`folder`</b> (str, optional):  folder path to get all items in folder, usually not ideal. Defaults to None. 
 - <b>`files`</b> (list, optional):  list with all file paths, ideal way to input files. Defaults to None. 
 - <b>`outdir`</b> (str, optional):  directory where all results will be saved. Defaults to '/tmp/'. 
 - <b>`perAmp`</b> (bool, optional):  run iraf per amplifier. Defaults to False. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterbias.py#L295"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `del_procfiles`

```python
del_procfiles()
```

Delete intermediate files  



---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterbias.py#L288"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getBPM`

```python
getBPM()
```

Generates Bad Pixel Mask (hotmask) for incombined result   



---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterbias.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `overscan`

```python
overscan(file, genThumb)
```

Run overscan routine 



**Args:**
 
 - <b>`file`</b> (str):  filename 
 - <b>`genThumb`</b> (bool):  generate image from result 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterbias.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_imcombine`

```python
run_imcombine(delete_after=True)
```

Run iraf IMCOMBINE on files loaded on class These files must be overscanned before running IRAF 



**Args:**
 
 - <b>`delete_after`</b> (bool, optional):  Delete intermediate files after done. Defaults to True. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/masterbias.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_overscan`

```python
run_overscan(genThumb=False)
```

Run overscan on files loaded to MasterBias Class 



**Args:**
 
 - <b>`genThumb`</b> (bool, optional):  Generate Image from done overscan file. Defaults to False. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
