from mar.config import MarManager

from files.views import scan
from files.auxs import get_master_path

from process.models import Operations
from .thread import *
from .reduction_proc import Reduction_Instance

from django.conf import settings
import os
import time

from files.models import CurrentConfig

def full_reduction(num, code):
    MarManager.INFO(f"Starting Full reduction process on Block {num}")

    Reduction_Instance.set_block_id(num)
    Reduction_Instance.set_code(code)

    MarManager.submit(Reduction_Instance.master_bias, group='MasterBias')
    MarManager.wait_group_done('MasterBias')

    MarManager.submit(Reduction_Instance.master_flat, group='MasterFlat')
    MarManager.wait_group_done('MasterFlat')

    MarManager.submit(Reduction_Instance.proccess_img, group='SciImage')
    MarManager.wait_group_done('SciImage')

    MarManager.INFO(f"Done Full reduction process on Block {num}")
    MarManager.write_final_log(filename=f"fullRed_block{num}.log")
    MarManager.clear_logs()

def bias(num, code):
    MarManager.INFO(f"Starting BIAS reduction process on Block {num}")
    MarManager.submit(Reduction_Instance.master_bias, num, code, group='MasterBias')
    MarManager.wait_group_done('MasterBias')

def flat(num, code):
    MarManager.INFO(f"Starting FLAT reduction process on Block {num}")
    MarManager.submit(Reduction_Instance.master_flat, num, code, group='MasterBias')
    MarManager.wait_group_done('MasterBias')

def sci(num, code):
    MarManager.INFO(f"Starting SCI reduction process on Block {num}")
    MarManager.submit(Reduction_Instance.proccess_img, num, code, group='MasterBias')
    MarManager.wait_group_done('MasterBias')

def fbyfilter(block, code):
    MarManager.INFO(f"Starting FLAT reduction process on Block by filter {block.id}")
    MarManager.submit(Reduction_Instance.processFlatByFilter, block, code, group='MasterFlatByFilter')
    MarManager.wait_group_done('MasterFlatByFilter')

def sbyfilter(block, code):
    MarManager.INFO(f"Starting SCI by filter reduction process on Block by filter {block.id}")
    MarManager.submit(Reduction_Instance.processSciByFilter, block, code, group='MasterSciByFilter')
    MarManager.wait_group_done('MasterSciByFilter')


def process_reduction(request):
    if 'id' not in request.data:
        return "Must provide ID of reduction block!"
    num = int(request.data['id'])
    code = None
    if 'code' in request.data:
        code = request.data['code']
    Reduction_Instance.addTask('fullreduction', num, code)
    return f"Starting Full reduction process on Block {num}"


def pflatbyfilter(block, code):
    Reduction_Instance.addTask('flatbyfilter', block, code)
    return "Starting reduction process on flatbyfilter block"

def pscibyfilter(block, code):
    Reduction_Instance.addTask('scibyfilter', block, code)
    return "Starting reduction process on scibyfilter block"


def process_bias(request):
    if 'id' not in request.data:
        return "Must provide ID of reduction block!"
    num = int(request.data['id'])
    code = None
    if 'code' in request.data:
        code = request.data['code']
    Reduction_Instance.addTask('bias', num, code)
    return f"Starting Bias process on Block {num}"

def process_flat(request):
    if 'id' not in request.data:
        return "Must provide ID of reduction block!"
    num = int(request.data['id'])
    code = None
    if 'code' in request.data:
        code = request.data['code']
    Reduction_Instance.addTask('flat', num, code)
    return f"Starting Flat process on Block {num}"

def process_sci(id, code):
    Reduction_Instance.addTask('sci', int(id), code)
    return f"Starting SCI process on Block {id}"

def scan_folder(request):
    if 'path' not in request.data:
        return {"Must provide path!"}

    if not 'contains' in request.data:
        Reduction_Instance.addTask('scan', str(request.data['path'].strip()), None)
    else:
        Reduction_Instance.addTask('scan', str(request.data['path'].strip()), str(request.data['contains']))
    return {"msg": "Scanning..."}


def is_subpath(path, potential_parent):
    path = os.path.abspath(path)
    potential_parent = os.path.abspath(potential_parent)
    return os.path.commonpath([path]) == os.path.commonpath([path, potential_parent])

def doScan(path, contains=None):
    if not is_subpath(path, settings.ROOTFITS):
        path = os.path.join(settings.ROOTFITS, path)

    files = absoluteFilePaths(path)
    Reduction_Instance.set_status('Scanning')

    for file in files:
        if contains is not None:
            if contains in file:
                MarManager.submit(scan, file, group = 'scan')
        if contains is None:
            MarManager.submit(scan, file, group = 'scan')
    
    try: MarManager.wait_group_done('scan')
    except: pass

    Reduction_Instance.set_status()

def queueRunner(task):
    if (task):
        conf = CurrentConfig.objects.filter(current = True).first()
        MarManager.INFO(f"Starting {task['function']} process on Block {task['block']}")
        MarManager.INFO(f"Running with {conf.name}")

        try: task['block'] = int(task['block'])
        except: pass
        
        if task['function'] == 'bias':
            bias(task['block'], task['code'])
        
        if task['function'] == 'flat':
            flat(task['block'], task['code'] )

        if task['function'] == 'sci':
            sci(task['block'], task['code'])

        if task['function'] == 'fullreduction':
            full_reduction(task['block'], task['code'])
        
        if task['function'] == 'flatbyfilter':
            fbyfilter(task['block'], task['code'])
        
        if task['function'] == 'scibyfilter':
            sbyfilter(task['block'], task['code'])

        if task['function'] == 'scan':
            doScan(task['block'], task['code'])

        path = os.path.join(get_master_path("LOGS"), str(round(time.time())) + '.txt')
        
        MarManager.finishLog(path)
        operation = str(task['function']) + ' ' + str(task['block']) + ' ' + str(task['code'])
        op = Operations(endDate = datetime.date, logPath = removeRootFitsPath(path), operation = operation)
        op.save()

        Reduction_Instance.walkQueue()

import threading

def runQueue():
    while True:
        if Reduction_Instance.get_statuc() == 'Available':
            
            task = Reduction_Instance.getFirstQueue()
            t = threading.Thread(target=queueRunner, args=[task])
            t.start()
            t.join()

        time.sleep(1)


t = threading.Thread(target=runQueue)
t.setDaemon(True)
t.start()
