from fileinput import filename
from django.shortcuts import render
import os

from files.checks import run_checks, create_12_band_im
from .models import *
from datetime import datetime, timedelta
from astropy.io import fits
# Create your views here.

from .auxs import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.response import Response
from django.db.utils import IntegrityError, OperationalError

import pytz
from mar.config import MarManager

import time
from django.conf import settings

@api_view(['POST'])
def scanFolder(request):
    if 'path' not in request.data:
        return Response("Must provide path!")

    files = absoluteFilePaths(request.data['path'])
    error = "Error on: "
    for file in files:
        res = addFile(file, checkFolder=False)
        if res != "Success":
            error += f'{file}, '
    if error != "Error on: ":
        return Response(error)
    return Response("Success")


def scan(file):
    res = addFile(file, checkFolder=False)

    if res:
        if res != "Success":
            MarManager.WARN(f"Error adding {file}")
        if res == "Success":
            MarManager.INFO(f"Added {file}")


@api_view(['POST'])
def addNewFile(request):
    if 'path' not in request.data:
        return Response("Must provide path!")
    res = addFile(request.data["path"], checkFolder=False)
    return Response(res)

def is_subpath(path, base_path):
    relpath = os.path.relpath(path, base_path)
    return not (relpath == os.curdir or relpath.startswith(os.pardir))

def is_file_in_directory(file_path, directory_path):
    # Get the absolute paths of the file and the directory
    file_path = os.path.abspath(file_path)
    directory_path = os.path.abspath(directory_path)

    # Check if the file path starts with the directory path
    return file_path.startswith(directory_path)

def addFile(filepath, filename = None, tipo=None, retur = False, movefile=False, checkFolder = True):
    if not is_file_in_directory(filepath, settings.ROOTFITS):
        filepath = getFilePathRootFits(filepath)

    MarManager.INFO(f"Adding {filepath}")
    filename = get_filename(filepath, strip=True)
    
    if not checkFolder:
        for typ in settings.TYPES:
            if is_subpath(filepath, get_master_path(typ)):
                return

    file = IndividualFile.objects.filter(file_name = filename).first()
    if file:
        MarManager.INFO(f"{file} already exists on DB")
        return

    header = fits.getheader(filepath)

    ext = 0
    if len(header) < 12:
        ext = 1
        header = fits.getheader(filepath, ext)

    try:
        data = datetime.strptime(header["DATE-OBS"], "%Y-%m-%dT%H:%M:%S.%f")
    except:
        data = None

    field = get_field(header)
    filter = get_filter(header)
    exptime = get_exptime(header)

    if tipo is None:
        tipo = get_type(header)

        if movefile:
            path = move_file(filepath, data, tipo, filter)
            if path is None:
                path = filepath
        else:
            path = filepath
    else:
        path = filepath

    path = removeRootFitsPath(path)

    #MarManager.INFO(f"infos {data} {tipo} {filter}")
    file = IndividualFile(obsDate = data, exptime = exptime,  field = field, file_type=tipo, band = filter, file_name = filename, file_path = path)
    
    saved = False
    while not saved:
        try:
            file.save()
            saved = True
        except IntegrityError as e:
            if tipo in ["FLAT", "BIAS", "SCI"]:
                os.remove(getFilePathRootFits(path))
            return e
        except OperationalError as e:
            time.sleep(0.3)

    if retur:
        return file
    return "Success"

@api_view(['POST', 'GET'])
def createBiasBlock(request):
    res = createBias(request)
    return Response(res)

def createBias(request):
    if 'startDate' not in request.data:
        return "Must provide startDate!"
    if 'endDate' not in request.data:
        return "Must provide endDate!"

    endDate = datetime.strptime(request.data['endDate'], "%Y-%m-%d") + timedelta(days=1)
    res = IndividualFile.objects.filter(obsDate__range=[request.data['startDate'], endDate], file_type="BIAS", isvalid=1).all()
    ## endDate do not include itself

    masterPath = get_master_path("BIAS")
    block = BiasBlock(blockStartDate=request.data['startDate'], blockEndDate=endDate)

    block.save()
    for i in res:
        block.bias.add(i)

    return {"msg": "Created block with: " + str(len(res)) + " BIAS", "id": block.id}

@api_view(['POST'])
def createFlatBlock(request):
    res = createFlat(request)
    return Response(res)

def createFlat(request):
    if 'startDate' not in request.data:
        return "Must provide startDate!"
    if 'endDate' not in request.data:
        return "Must provide endDate!"

    startDate = request.data['startDate']
    endDate = datetime.strptime(request.data['endDate'], "%Y-%m-%d") + timedelta(days=1)

    block = FlatsBlock(blockStartDate=startDate, blockEndDate=endDate)
    block.save()

    bands = {'R': '', 'G': '', 'I': '', 'Z': '', 'U': '', 'F378': '', 'F395': '', 'F410': '', 'F430': '', 'F515': '', 'F660': '', 'F861': ''}
    for band in bands:

        filter = FlatByFilter(blockStartDate=startDate, blockEndDate=endDate, band=band)
        filter.save()

        if 'nameContains' in request.data:
            flat = IndividualFile.objects.filter(file_name__contains=request.data['nameContains'], file_type="FLAT", band=band, obsDate__range=[startDate, endDate], isvalid=1).all()
        else:
            flat = IndividualFile.objects.filter(file_type="FLAT", band=band, obsDate__range=[startDate, endDate], isvalid=1).all()
        
        for f in flat:
            filter.flats.add(f)

        block.flatsByFilter.add(filter)

    return {"msg": "Created flat block with all bands blocks.", "id": block.id}


def createFlatByFilter(request):
    startDate = request.data['startDate']
    endDate = datetime.strptime(request.data['endDate'], "%Y-%m-%d") + timedelta(days=1)

    filter = FlatByFilter(band=request.data['band'], blockStartDate=startDate, blockEndDate=endDate)
    filter.save()

    if 'field' in request.data:
        flats = IndividualFile.objects.filter(file_type="FLAT", band=request.data['band'], field=request.data['field'],
                                              obsDate__range=[startDate, endDate], isvalid=1).all()
    elif 'nameContains' in request.data:
        flats = IndividualFile.objects.filter(file_name__contains=request.data['nameContains'], file_type="FLAT", band=request.data['band'], field=request.data['field'],
                                              obsDate__range=[startDate, endDate], isvalid=1).all()
    else:
        flats = IndividualFile.objects.filter(file_type="FLAT", band=request.data['band'],
                                              obsDate__range=[startDate, endDate], isvalid=1).all()

    for f in flats:
        filter.flats.add(f)

    filter.save()
    return {"msg": "Created flat by filter block.", "id": filter.id}

@api_view(['POST'])
def createSciBlock(request):
    res = createSci(request)
    return Response(res)

def createSci(request):
    if 'startDate' not in request.data:
        return "Must provide startDate!"
    if 'endDate' not in request.data:
        return "Must provide endDate!"

    startDate = request.data['startDate']
    endDate = datetime.strptime(request.data['endDate'], "%Y-%m-%d") + timedelta(days=1)
    block = SciBlock(blockStartDate=startDate, blockEndDate=endDate)
    block.save()

    bands = {'R': '', 'G': '', 'I': '', 'Z': '', 'U': '', 'F378': '', 'F395': '', 'F410': '', 'F430': '', 'F515': '',
             'F660': '', 'F861': ''}
    for band in bands:
        filter = SciByFilter(band=band, blockStartDate=startDate, blockEndDate=endDate)
        filter.save()

        if 'field' in request.data:
            '''Deprecated condition, not used in front end'''
            scies = IndividualFile.objects.filter(file_type="SCI", band=band, field=request.data['field'], obsDate__range=[startDate, endDate]).all()
        elif 'nameContains' in request.data:
            names = request.data['nameContains'].replace(' ', '').split(',')
            scies = []
            for name in names:
                tmp = IndividualFile.objects.filter(file_name__contains=name, file_type="SCI", band=band, obsDate__range=[startDate, endDate]).all()
                scies = scies + list(tmp)
        else:
            scies = IndividualFile.objects.filter(file_type="SCI", band=band, obsDate__range=[startDate, endDate]).all()

        
        for s in scies:
            filter.scies.add(s)
            dbFile = IndividualFile.objects.filter(file_name="proc_" + s.file_name).first()
            if dbFile is not None:
                filter.processed.add(dbFile)
            dbFile = None

        block.sciByFilter.add(filter)

    return {"msg": "Created sci block with all bands blocks.", "id": block.id}

def createSciByFilter(request):
    startDate = request.data['startDate']
    endDate = datetime.strptime(request.data['endDate'], "%Y-%m-%d") + timedelta(days=1)

    filter = SciByFilter(band=request.data['band'], blockStartDate=startDate, blockEndDate=endDate)
    filter.save()

    if 'field' in request.data:
        scies = IndividualFile.objects.filter(file_type="SCI", band=request.data['band'], field=request.data['field'], obsDate__range=[startDate, endDate], isvalid=1).all()
    elif 'nameContains' in request.data:
        names = request.data['nameContains'].replace(' ', '').split(',')
        scies = []
        for name in names:
            tmp = IndividualFile.objects.filter(file_name__contains=name, file_type="SCI", band=request.data['band'], obsDate__range=[startDate, endDate], isvalid=1).all()
            scies = scies + list(tmp)
    else:
        scies = IndividualFile.objects.filter(file_type="SCI", band=request.data['band'], obsDate__range=[startDate, endDate], isvalid=1).all()

    for s in scies:
        filter.scies.add(s)

        dbFile = IndividualFile.objects.filter(file_name="proc_" + s.file_name).first()
        if dbFile is not None:
            filter.processed.add(dbFile)
        dbFile = None

    filter.save()
    return {"msg": "Created sci by filter block.", "id": filter.id}

@api_view(['POST'])
def createReductionBlock(request):
    res = createReduction(request)
    return Response(res)

def createReduction(request):
    if 'bias_block_id' not in request.data:
        return "Must provide bias_block_id!"
    if 'flat_block_id' not in request.data:
        return "Must provide flat_block_id!"
    if 'sci_block_id' not in request.data:
        return "Must provide sci_block_id!"

    bias = int(request.data['bias_block_id'])
    flat = int(request.data['flat_block_id'])
    sci = int(request.data['sci_block_id'])
    sci = SciBlock.objects.filter(id=sci).first()

    startDate = sci.blockStartDate
    endDate = sci.blockEndDate

    block = ReductionBlock(biasBlock_id=bias, flatsBlock_id=flat, sciBlock_id=sci.id, startDate=startDate, endDate=endDate)
    block.save()

    return {"msg": "Created reduction block with success.", "id": block.id}


@api_view(['POST'])
def request_twelve_band_im(request):
    if 'field' not in request.data:
        return Response("Must provide field!")
    
    MarManager.submit(create_12_band_im, request['field'])
    return Response({"msg": "Submitted job to create 12 band images."})

# from files.models import FlatByFilter, IndividualFile
# z = IndividualFile.objects.filter(file_type='FLAT').all()

# for i in z:
#     print(z.delete())

run_checks()
