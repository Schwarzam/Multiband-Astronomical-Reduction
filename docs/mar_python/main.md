<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `main`




**Global Variables**
---------------
- **version__**
- **ABS_PATH**
- **env**

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `dumpconfig`

```python
dumpconfig(_config, outfile)
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `loadconfig`

```python
loadconfig(file)
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AttributeDict`




<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(d)
```









---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Enviroment`
A class that represents the configuration of the MAR package. 



**Attributes:**
 
 - <b>`marPath`</b> (str):  The absolute path to the default configuration file. 
 - <b>`marConf`</b> (AttributeDict):  A dictionary-like object that holds the configuration values  loaded from the configuration file. 

Methods: 
 - <b>`welcome`</b> ():  Prints a welcome message to the console if this is the first time the  package is being used. 
 - <b>`getConf`</b> ():  Returns the configuration values stored in `marConf`. 
 - <b>`setItemConf`</b> (section: str, item: str, value: Any):  Sets the value of a specific configuration  item in the specified section. 
 - <b>`saveConf`</b> ():  Saves the current configuration values to the configuration file. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getConf`

```python
getConf()
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L71"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_config`

```python
load_config(path)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L106"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `saveConf`

```python
saveConf()
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `setItemConf`

```python
setItemConf(section, item, value)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/main.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `welcome`

```python
welcome()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
