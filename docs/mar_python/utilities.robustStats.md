<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/robustStats.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utilities.robustStats`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/robustStats.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `purge_outliers`

```python
purge_outliers(x, n_sigma=3.0, n=5, med=False)
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/robustStats.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `std_robust`

```python
std_robust(x, n_sigma=3.0, n=5)
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/robustStats.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `arrStats`

```python
arrStats(arr)
```

Computes various statistics for an input array. 



**Args:**
 
 - <b>`arr`</b> (numpy array):  The input array. 



**Returns:**
 
 - <b>`tuple`</b>:  A tuple containing the mode, median, mean, standard deviation, minimum, and maximum values of the input  array. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/robustStats.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `robustStat`

```python
robustStat(arr, sigma=3, iters=5, med=False)
```

Computes various robust statistics for an input array. 



**Args:**
 
 - <b>`arr`</b> (numpy array):  The input array. 
 - <b>`sigma`</b> (float, optional):  The number of standard deviations allowed for data to be considered as outlier.  Defaults to 3. 
 - <b>`iters`</b> (int, optional):  The number of iterations to perform the outlier rejection process. Defaults to 5. array. If not None, this overrides the `sigma` and `iters` parameters. Defaults to None. 
 - <b>`med`</b> (bool, optional):  If True, use the median absolute deviation (MAD) instead of the standard deviation for  outlier rejection. Defaults to False. 



**Returns:**
 
 - <b>`dict`</b>:  A dictionary containing the maximum, minimum, mean, median, standard deviation, fraction of rejected  data points, robust standard deviation (nmad), and robust standard deviation (rms) of the input array. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
