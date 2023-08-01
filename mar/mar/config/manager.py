from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
import threading
import inspect

import os
from datetime import datetime

import mar
import time
import tempfile

import psutil

from threading import Lock

try:
    configVal = mar.AttributeDict(mar.env.marConf.config)
except:
    print('Could not get Instrument conf.')


global MarManager, MarProcess
MarPr = MarManager = None


class MarProcess(ProcessPoolExecutor):
    def __init__(self, max_workers, thread_name_prefix, logdir = '/tmp'):
        ProcessPoolExecutor.__init__(self, max_workers)
        self.lock = Lock()

        self.logdir = logdir
        self.tasks = {'general': []}
        self.log = {}

        self.workers = max_workers

    def submit(self, fn, *args, group = "general", **kwargs):
        future = super().submit(fn, *args, **kwargs)
        future.add_done_callback(worker_callbacks)
        if group not in self.tasks:
            self.tasks[group] = []
        self.tasks[group].append(future)


    def wait_group_done(self, group = "general"):
        queue = [i.done() for i in self.tasks[group]]
        
        while False in queue:
            time.sleep(0.2)
            queue = [i.done() for i in self.tasks[group]]

    

class MarThreads(ThreadPoolExecutor):
    """Custom thread manager.

    This class is an extension of the ThreadPoolExecutor class from the concurrent.futures
    module, which allows for the execution of multiple tasks simultaneously in threads.

    The MarThreads class was created to manage the threads used by the Mar system. It provides
    methods for submitting tasks for execution in threads, monitoring the progress of tasks,
    generating logs, and other related functionalities.

    Args:
        max_workers (int): Maximum number of threads that can be executed simultaneously.
        thread_name_prefix (str): Prefix to be added to the name of the created threads.
        MarP (MarProcess): Instance of the MarProcess class to manage processes.
        logdir (str, optional): Directory where the logs will be stored. Defaults to '/tmp'.
        debug (bool, optional): Indicates whether debug mode is enabled. Defaults to False.

    Attributes:
        logdir (str): Directory where the logs are stored.
        tasks (dict): Dictionary that contains the tasks submitted for execution in threads.
        _thread_name_prefix (str): Prefix added to the name of the created threads.
        logname (str): Name of the log file.
        log (str): Full path of the log file.
        workers (int): Maximum number of threads that can be executed simultaneously.
        MarP (MarProcess): Instance of the MarProcess class to manage processes.
        debug (bool): Indicates whether debug mode is enabled.

    Methods:
        submit(fn, *args, group='general', **kwargs):
            Submits a task for execution in a thread.

        submit_process(fn, *args, group='general', **kwargs):
            Submits a task for execution in a process.

        wait_process(group):
            Waits for the execution of all tasks in a specific process group.

        get_queue_process(group='general'):
            Returns a list indicating whether the tasks in a specific process group are completed.

        get_logs():
            Returns the contents of the log file.

        INFO(content):
            Adds a log entry with an INFO level.

        WARN(content):
            Adds a log entry with a WARNING level.

        CRITICAL(content):
            Adds a log entry with a CRITICAL level.

        DEBUG(content):
            Adds a log entry with a DEBUG level, if debug mode is enabled.

        wLog(content, tipo='INFO'):
            Adds a log entry with the specified level.

        wait_group_done(group='general'):
            Waits for the execution of all tasks in a specific thread group.

        clear_logs():
            Clears the log file.

        finishLog(filename):
            Copies the current log file to a new location and clears the original file.

    """
    def __init__(self, max_workers, thread_name_prefix, MarP, logdir = '/tmp', debug=False):
        ThreadPoolExecutor.__init__(self, max_workers)
        self.lock = Lock()
        
        self.logdir = logdir
        self.tasks = {'general': []}
        self._thread_name_prefix = thread_name_prefix
        self.logname = 'mar.log'
        self.log = os.path.join(self.logdir, self.logname)
        
        self.workers = max_workers
        self.init_log()

        self.MarP = MarP
        
        self.debug = debug

    def init_log(self):
        io = open(self.log, 'a')
        io.close()
        
    def submit(self, fn, *args, group = "general", **kwargs):
        """Submits a task for execution in a thread.

        This method submits a task for execution in a thread managed by the MarThreads instance.
        The task can be any function or method that takes the specified arguments.

        Args:
            fn (function): Function or method to be executed.
            *args: Positional arguments to be passed to the function.
            group (str, optional): Group name to associate the task with. Default is 'general'.
            **kwargs: Keyword arguments to be passed to the function.

        Returns:
            Future: A concurrent.futures.Future object representing the execution of the submitted task.

        Raises:
            TypeError: If the submitted task is not a function or method.
            concurrent.futures._base.CancelledError: If the task was cancelled before completion.
            concurrent.futures._base.TimeoutError: If the task exceeded the specified timeout limit.

        """
        future = super().submit(fn, *args, **kwargs)
        future.add_done_callback(worker_callbacks)
        if group not in self.tasks:
            self.tasks[group] = []
        self.tasks[group].append(future)

    def submit_process(self, fn, *args, group = "general", **kwargs):
        try:
            self.MarP.submit(fn, *args, group = group, **kwargs)
        except BrokenProcessPool:
            mar.config.resetThreads()

    def wait_process(self, group):
        self.MarP.wait_group_done(group)

    def get_queue_process(self, group = 'general'):
        return [i.done() for i in self.MarP.tasks[group]]
        
    def get_logs(self):
        f = open(self.log, 'r')
        return f.read()
    
    def get_queue(self, group = 'general'):
        return [i.done() for i in self.tasks[group]]
    
    def INFO(self, content):
        self.wLog(content, "INFO")
    def TIME(self, content):
        self.wLog(content, "TIME")
    def WARN(self, content):
        self.wLog(content, "WARNING")
    def CRITICAL(self, content):
        self.wLog(content, "CRITICAL")
    def DEBUG(self, content):
        if self.debug:
            self.wLog(content, "DEBUG")
    
    
    def wLog(self, content, tipo="INFO"):
        p = psutil.Process(os.getpid())

        if p.nice() < 10:
            p.nice(10)

        func = inspect.currentframe().f_back.f_back.f_code
        function = func.co_name
        filename = func.co_filename

        name = threading.current_thread().name

        with self.lock:
            io = open(self.log, 'a')
            io.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - PID {os.getpid()} - {name} - {tipo} - {filename.split('/')[-1]} - {function}() - {str(content)} \n")
            io.close()
    

    def wait_group_done(self, group = "general"):
        """Waits for the execution of all tasks in a specific thread group.

        This method blocks the calling thread until all tasks submitted to the specified group are
        completed. It periodically checks the status of the tasks to determine if they are done.

        Args:
            group (str, optional): Group name to wait for. Default is 'general'.

        Raises:
            concurrent.futures._base.CancelledError: If any of the tasks in the group was cancelled
                before completion.
            concurrent.futures._base.TimeoutError: If any of the tasks in the group exceeded the
                specified timeout limit.

        """
        if group not in self.tasks:
            return
        queue = [i.done() for i in self.tasks[group]]
        
        while False in queue:
            time.sleep(0.2)
            queue = [i.done() for i in self.tasks[group]]

    def clear_logs(self):
        io = open(self.log, 'w')
        io.close()

    def finishLog(self, filename):
        os.system(f'cp {self.log} {filename}')
        self.clear_logs()



def worker_callbacks(f):
    e = f.exception()

    if e is None:
        return

    trace = []
    tb = e.__traceback__
    while tb is not None:
        trace.append({
            "filename": tb.tb_frame.f_code.co_filename,
            "name": tb.tb_frame.f_code.co_name,
            "lineno": tb.tb_lineno
        })
        tb = tb.tb_next
    
    MarManager.CRITICAL(f"""{type(e).__name__}, {str(e)}, {trace}""")

try:
    MarPr = MarProcess(max_workers=int(configVal.PROCESSES), thread_name_prefix="thread")
except:
    MarPr = MarProcess(max_workers=int(configVal.PROCESSES), thread_name_prefix="thread", logdir=tempfile.TemporaryFile().name.rsplit('\\', 1)[0].rsplit('/', 1)[0])

try:
    MarManager = MarThreads(max_workers=int(configVal.THREADS), thread_name_prefix="thread", MarP=MarPr)
except:
    MarManager = MarThreads(max_workers=int(configVal.THREADS), thread_name_prefix="thread", MarP=MarPr, logdir=tempfile.TemporaryFile().name.rsplit('\\', 1)[0].rsplit('/', 1)[0])



def resetThreads():
    mar.config.MarManager = None
    mar.config.MarPr = None
    
    try:
        MarPr = MarProcess(max_workers=int(configVal.PROCESSES), thread_name_prefix="thread")
    except:
        MarPr = MarProcess(max_workers=int(configVal.PROCESSES), thread_name_prefix="thread", logdir=tempfile.TemporaryFile().name.rsplit('\\', 1)[0].rsplit('/', 1)[0])


    try:
        mar.config.MarManager = MarThreads(max_workers=int(configVal.THREADS), thread_name_prefix="thread", MarP=MarPr)
    except:
        mar.config.MarManager = MarThreads(max_workers=int(configVal.THREADS), thread_name_prefix="thread", MarP=MarPr, logdir=tempfile.TemporaryFile().name.rsplit('\\', 1)[0].rsplit('/', 1)[0])
