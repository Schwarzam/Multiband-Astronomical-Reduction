<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/stats.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utilities.stats`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/stats.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `MAD`

```python
MAD(arr, axis=None)
```

Calculate the Median Absolute Deviation (MAD) of an array. 



**Parameters:**
 
----------- arr : array-like  Input data. 



**Returns:**
 
-------- res : array or float  MAD of the input array. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/stats.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `interpolate`

```python
interpolate(arr, sigma)
```

Interpolates outliers in the input array by replacing them with the interpolated values from the nearest non-outlier values. 

Parameters 
---------- arr : array_like  The input array of values to be interpolated. sigma : float  The number of standard deviations to use as the clipping limit  when identifying outliers. 

Returns 
------- np.ndarray  The interpolated array. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/stats.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `median_robust`

```python
median_robust(arr, axis=None, sigma=3, maxiters=1)
```

Calculate the median value of an array with robust estimation. 

The median is calculated using a robust estimator that iteratively sigma-clips the data to remove outliers. 



**Args:**
 
 - <b>`arr`</b> (array-like):  Input data. 
 - <b>`axis`</b> (int, tuple):  Axis or axes along which to perform the operation. Default is None. 
 - <b>`sigma`</b> (float):  The number of standard deviations to use for clipping. Default is 3. 
 - <b>`maxiters`</b> (int):  The maximum number of iterations to perform. Default is 1. 



**Returns:**
 
 - <b>`float or ndarray`</b>:  The median of the input array. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/stats.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `mean_robust`

```python
mean_robust(arr, axis=None, sig=3, iters=2)
```

Calculate the mean value of an array with robust estimation. 

The mean is calculated using a robust estimator that iteratively sigma-clips the data to remove outliers. 



**Args:**
 
 - <b>`arr`</b> (array-like):  Input data. 
 - <b>`axis`</b> (int, tuple):  Axis or axes along which to perform the operation. Default is None. 
 - <b>`sig`</b> (float):  The number of standard deviations to use for clipping. Default is 3. 
 - <b>`iters`</b> (int):  The maximum number of iterations to perform. Default is 2. 



**Returns:**
 
 - <b>`float or ndarray`</b>:  The mean of the input array. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/stats.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `mean_robust2`

```python
mean_robust2(arr, axis=None, sig=3, iters=1)
```

Calculate the mean value of an array with robust estimation. 

The mean is calculated using a robust estimator that iteratively sigma-clips the data to remove outliers. 



**Args:**
 
 - <b>`arr`</b> (array-like):  Input data. 
 - <b>`axis`</b> (int, tuple):  Axis or axes along which to perform the operation. Default is None. 
 - <b>`sig`</b> (float):  The number of standard deviations to use for clipping. Default is 3. 
 - <b>`iters`</b> (int):  The maximum number of iterations to perform. Default is 1. 



**Returns:**
 
 - <b>`float`</b>:  The mean of the input array. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/stats.py#L120"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `purge_outliers`

```python
purge_outliers(x, n_sigma=3.0, n=5, med=False)
```

Returns a filtered version of the input array x that removes any values more than n_sigma standard deviations away from the median, where the median and standard deviation are computed using the median absolute deviation (MAD). 



**Args:**
 
 - <b>`x`</b> (numpy.ndarray):  Input array to be filtered. 
 - <b>`n_sigma`</b> (float):  Number of standard deviations away from the median to consider as an outlier. 
 - <b>`n`</b> (int):  Number of iterations of outlier removal to perform. 
 - <b>`med`</b> (bool):  If True, use the median of x instead of the mean to compute the MAD. 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  Filtered version of the input array x. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/stats.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `std_robust`

```python
std_robust(x, n_sigma=3.0, n=5)
```

Calculate the robust standard deviation of an array along a specified axis. 



**Parameters:**
 x (array_like): Input data. n_sigma (float, optional): The number of standard deviations to use as a threshold for outliers. Default is 3. n (int, optional): The number of iterations used to remove outliers. Default is 5. 



**Returns:**
 float or ndarray: The robust standard deviation of the input array. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
