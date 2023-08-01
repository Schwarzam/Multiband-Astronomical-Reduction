<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/swarp.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `wrappers.swarp`






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/swarp.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Swarp`
A class to run the SWarp software for creating co-added images from multiple input images. 



**Args:**
 
 - <b>`image`</b> (str, optional):  The name of the input FITS image to be co-added. Default is None. 
 - <b>`addconf`</b> (dict, optional):  Additional configuration parameters to add to the default configuration. Default is None. 
 - <b>`defaultconf`</b> (dict, optional):  A dictionary of the entire configuration, to overwrite all of the default configuration. 
 - <b>`read_addconf`</b> (str, optional):  A path to a file containing a configuration dictionary to add to the default configuration. 
 - <b>`read_defaultconf`</b> (str, optional):  A path to a file containing a dictionary of the entire configuration, to overwrite all of the default configuration.  
 - <b>`outdir`</b> (str, optional):  The output directory for the co-added FITS image. Default is '/tmp/'. 
 - <b>`command`</b> (str, optional):  The SWarp executable command to use. Default is 'swarp'. 



**Attributes:**
 
 - <b>`command`</b> (str):  The SWarp executable command to use. 
 - <b>`image`</b> (str):  The name of the input FITS image to be co-added. 
 - <b>`path`</b> (str):  The output directory for the co-added FITS image. 
 - <b>`config`</b> (dict):  A dictionary of the default SWarp configuration parameters and their default values. 

Methods: 
 - <b>`run`</b> (self):  Runs SWarp on the input FITS image with the current configuration parameters. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/swarp.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    image=None,
    addconf=None,
    defaultconf=None,
    read_addconf=None,
    read_defaultconf=None,
    outdir='/tmp/',
    command='swarp'
)
```

Initializes a new instance of the Swarp class with the specified input FITS image, additional configuration parameters, default configuration dictionary, configuration file paths, output directory and SWarp executable command. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/wrappers/swarp.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run()
```

Runs SWarp on the input FITS image with the current configuration parameters.  






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
