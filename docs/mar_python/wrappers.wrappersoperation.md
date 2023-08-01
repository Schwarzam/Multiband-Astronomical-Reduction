<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/wrappersoperation.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `wrappers.wrappersoperation`






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/wrappersoperation.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `readWriteCats`
A class that provides methods for reading and writing configuration files for image processing tools. 



**Attributes:**
 
- config (dict): A dictionary containing the configuration parameters and their values. 

Methods: 
- write_file(filename, mode='sex'): Writes the configuration parameters to a file. 
- read_config(filename, overwrite_config=False): Reads the configuration parameters from a file. 
- write_params(): Writes the parameters to a file. 
- convert(dicti=None): Converts the configuration parameter values to a dictionary with values and comments. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/wrappersoperation.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```

Initializes a new instance of the `readWriteCats` class. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/wrappersoperation.py#L125"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `convert`

```python
convert(dicti=None)
```

Converts the configuration parameter values to a dictionary with values and comments. 



**Parameters:**
 
- dicti (dict): A dictionary to be converted to a dictionary with values and comments. 



**Returns:**
 
- A dictionary containing the configuration parameters and their values with comments. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/wrappersoperation.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `read_config`

```python
read_config(filename, overwrite_config=False)
```

Reads the configuration parameters from a file. 



**Parameters:**
 
- filename (str): The name of the file to read the configuration parameters from. 
- overwrite_config (bool): Whether or not to overwrite the current configuration with the values read from the file. 



**Returns:**
 
- None. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/wrappersoperation.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_file`

```python
write_file(filename, mode='sex')
```

Writes the configuration parameters to a file. 



**Parameters:**
 
- filename (str): The name of the file to write the configuration parameters to. 
- mode (str): The mode in which to write the file. Can be 'sex' or 'scamp'. 



**Returns:**
 
- None. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/wrappersoperation.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_params`

```python
write_params()
```

Writes the parameters to a file. 



**Returns:**
 
- None. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
