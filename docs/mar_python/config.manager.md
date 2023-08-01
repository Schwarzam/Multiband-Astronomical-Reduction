<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `config.manager`




**Global Variables**
---------------
- **MarPr**
- **MarManager**

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L255"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `worker_callbacks`

```python
worker_callbacks(f)
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L285"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `resetThreads`

```python
resetThreads()
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MarProcess`




<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(max_workers, thread_name_prefix, logdir='/tmp')
```








---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `submit`

```python
submit(fn, *args, group='general', **kwargs)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `wait_group_done`

```python
wait_group_done(group='general')
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MarThreads`
Custom thread manager. 

This class is an extension of the ThreadPoolExecutor class from the concurrent.futures module, which allows for the execution of multiple tasks simultaneously in threads. 

The MarThreads class was created to manage the threads used by the Mar system. It provides methods for submitting tasks for execution in threads, monitoring the progress of tasks, generating logs, and other related functionalities. 



**Args:**
 
 - <b>`max_workers`</b> (int):  Maximum number of threads that can be executed simultaneously. 
 - <b>`thread_name_prefix`</b> (str):  Prefix to be added to the name of the created threads. 
 - <b>`MarP`</b> (MarProcess):  Instance of the MarProcess class to manage processes. 
 - <b>`logdir`</b> (str, optional):  Directory where the logs will be stored. Defaults to '/tmp'. 
 - <b>`debug`</b> (bool, optional):  Indicates whether debug mode is enabled. Defaults to False. 



**Attributes:**
 
 - <b>`logdir`</b> (str):  Directory where the logs are stored. 
 - <b>`tasks`</b> (dict):  Dictionary that contains the tasks submitted for execution in threads. 
 - <b>`_thread_name_prefix`</b> (str):  Prefix added to the name of the created threads. 
 - <b>`logname`</b> (str):  Name of the log file. 
 - <b>`log`</b> (str):  Full path of the log file. 
 - <b>`workers`</b> (int):  Maximum number of threads that can be executed simultaneously. 
 - <b>`MarP`</b> (MarProcess):  Instance of the MarProcess class to manage processes. 
 - <b>`debug`</b> (bool):  Indicates whether debug mode is enabled. 

Methods: submit(fn, *args, group='general', **kwargs):  Submits a task for execution in a thread. 

submit_process(fn, *args, group='general', **kwargs):  Submits a task for execution in a process. 

wait_process(group):  Waits for the execution of all tasks in a specific process group. 

get_queue_process(group='general'):  Returns a list indicating whether the tasks in a specific process group are completed. 

get_logs():  Returns the contents of the log file. 

INFO(content):  Adds a log entry with an INFO level. 

WARN(content):  Adds a log entry with a WARNING level. 

CRITICAL(content):  Adds a log entry with a CRITICAL level. 

DEBUG(content):  Adds a log entry with a DEBUG level, if debug mode is enabled. 

wLog(content, tipo='INFO'):  Adds a log entry with the specified level. 

wait_group_done(group='general'):  Waits for the execution of all tasks in a specific thread group. 

clear_logs():  Clears the log file. 

finishLog(filename):  Copies the current log file to a new location and clears the original file. 

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L123"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(max_workers, thread_name_prefix, MarP, logdir='/tmp', debug=False)
```








---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L196"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CRITICAL`

```python
CRITICAL(content)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L198"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `DEBUG`

```python
DEBUG(content)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `INFO`

```python
INFO(content)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L192"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `TIME`

```python
TIME(content)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `WARN`

```python
WARN(content)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L245"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_logs`

```python
clear_logs()
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L249"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `finishLog`

```python
finishLog(filename)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L183"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_logs`

```python
get_logs()
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_queue`

```python
get_queue(group='general')
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L180"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_queue_process`

```python
get_queue_process(group='general')
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L140"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `init_log`

```python
init_log()
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `submit`

```python
submit(fn, *args, group='general', **kwargs)
```

Submits a task for execution in a thread. 

This method submits a task for execution in a thread managed by the MarThreads instance. The task can be any function or method that takes the specified arguments. 



**Args:**
 
 - <b>`fn`</b> (function):  Function or method to be executed. 
 - <b>`*args`</b>:  Positional arguments to be passed to the function. 
 - <b>`group`</b> (str, optional):  Group name to associate the task with. Default is 'general'. 
 - <b>`**kwargs`</b>:  Keyword arguments to be passed to the function. 



**Returns:**
 
 - <b>`Future`</b>:  A concurrent.futures.Future object representing the execution of the submitted task. 



**Raises:**
 
 - <b>`TypeError`</b>:  If the submitted task is not a function or method. 
 - <b>`concurrent.futures._base.CancelledError`</b>:  If the task was cancelled before completion. 
 - <b>`concurrent.futures._base.TimeoutError`</b>:  If the task exceeded the specified timeout limit. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `submit_process`

```python
submit_process(fn, *args, group='general', **kwargs)
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L203"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `wLog`

```python
wLog(content, tipo='INFO')
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `wait_group_done`

```python
wait_group_done(group='general')
```

Waits for the execution of all tasks in a specific thread group. 

This method blocks the calling thread until all tasks submitted to the specified group are completed. It periodically checks the status of the tasks to determine if they are done. 



**Args:**
 
 - <b>`group`</b> (str, optional):  Group name to wait for. Default is 'general'. 



**Raises:**
 
 - <b>`concurrent.futures._base.CancelledError`</b>:  If any of the tasks in the group was cancelled  before completion. 
 - <b>`concurrent.futures._base.TimeoutError`</b>:  If any of the tasks in the group exceeded the  specified timeout limit. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/config/manager.py#L177"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `wait_process`

```python
wait_process(group)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
