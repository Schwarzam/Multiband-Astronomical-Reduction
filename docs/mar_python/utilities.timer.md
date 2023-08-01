<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/timer.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utilities.timer`




**Global Variables**
---------------
- **timer_t0**
- **timer_t1**


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/timer.py#L3"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `timeit`
A timer utility class that provides methods to measure elapsed time in minutes, seconds, and milliseconds. The class also has methods to reset the timer and sum the total elapsed time. 



**Attributes:**
 
 - <b>`start`</b> (float):  The timestamp when the timer was started. 
 - <b>`sum_timer`</b> (float):  The total elapsed time since the timer was created or reset. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/timer.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```

Initializes a new instance of the `timeit` class and starts the timer. 




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/timer.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `milliseconds`

```python
milliseconds(reset=False)
```

Calculates the elapsed time in milliseconds since the timer was started or reset. 



**Args:**
 
 - <b>`reset`</b> (bool):  If True, resets the timer to the current timestamp. 



**Returns:**
 
 - <b>`float`</b>:  The elapsed time in milliseconds, rounded to three decimal places. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/timer.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `minutes`

```python
minutes(reset=False)
```

Calculates the elapsed time in minutes since the timer was started or reset. 



**Args:**
 
 - <b>`reset`</b> (bool):  If True, resets the timer to the current timestamp. 



**Returns:**
 
 - <b>`float`</b>:  The elapsed time in minutes, rounded to one decimal place. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/timer.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `reset`

```python
reset()
```

Resets the timer to the current timestamp. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/timer.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `reset_all`

```python
reset_all()
```

Resets the timer to the current timestamp and resets the total elapsed time. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/timer.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `seconds`

```python
seconds(reset=False)
```

Calculates the elapsed time in seconds since the timer was started or reset. 



**Args:**
 
 - <b>`reset`</b> (bool):  If True, resets the timer to the current timestamp. 



**Returns:**
 
 - <b>`float`</b>:  The elapsed time in seconds, rounded to three decimal places. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/timer.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sum_minutes`

```python
sum_minutes()
```

Returns the total elapsed time in minutes. 



**Returns:**
 
 - <b>`float`</b>:  The total elapsed time in minutes, rounded to one decimal place. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/timer.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sum_timer_minutes`

```python
sum_timer_minutes(reset=True)
```

Calculates the elapsed time in minutes since the timer was started or reset and adds it to the total elapsed time. 



**Args:**
 
 - <b>`reset`</b> (bool):  If True, resets the timer to the current timestamp. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
