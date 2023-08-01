from django.shortcuts import render
from files.models import FinalTiles, IndividualFile

from process.models import Operations
from .reduction_proc import Reduction_Instance

from files.auxs import fpack, funpack

from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated

from mar import env
import os

import json
def stringify_dict_values(lst):
    return json.loads(json.dumps(lst, default=str))

# Create your views here.
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def get_queue(request):
    """This API view function retrieves the current queue from procRed instance.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """    
    queue = Reduction_Instance.getQueue()
    queue = stringify_dict_values(queue)
    return Response({'msg': queue})

# Create your views here.
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def remove_queue(request):
    if 'id' not in request.data:
        return Response({'error': 'Must include id in request'})

    Reduction_Instance.removeTask(request.data['id'])
    return Response({'msg': 'Task removed'})

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def get_conf(request):
    return Response({'msg': env.getConf()})

def parse_value(value):
    # Attempt to convert to boolean
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'
    
    if ',' in value:
        return [parse_value(v) for v in value.split(',')]

    # Attempt to convert to integer
    try:
        return int(value)
    except ValueError:
        pass

    # Return original string if conversion fails
    return value

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def set_item_conf(request):
    print(request)
    if 'section' not in request.data or 'item' not in request.data or 'value' not in request.data:
        return Response({'error': 'Must fill values.'})

    value = parse_value(request.data['value'])

    env.setItemConf(request.data['section'], request.data['item'], value)
    return Response({'msg': 'Set value.'})

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def get_operations(request):
    nums = 50
    if 'nums' in request.data:
        nums = int(request.data['nums'])

    res = Operations.objects.values().order_by('-id')[:nums]
    return Response({'msg': res})


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def get_operations_stats(request):

    final_count = FinalTiles.objects.count()
    fields_final = FinalTiles.objects.values('field').distinct().count()
    
    field_list = FinalTiles.objects.values('field').distinct()
    fields_with_twelve_filters = FinalTiles.objects.values('field')
    fields_with_twelve_filters = len([f['field'] for f in field_list 
        if len(fields_with_twelve_filters.filter(field=f['field'])) == 12])

    processed_count = IndividualFile.objects.filter(file_type="PROCESSED", status=5).count()
    processed_fields_count = IndividualFile.objects.filter(file_type="PROCESSED", status=5).values('field').distinct().count()

    return Response({'msg': 
                        {
                        'Final Tiles Count': final_count, 
                        'Fields With Coaddeds': fields_final,
                        'Done Processed Images': processed_count,
                        #'Fields With Done Processed': processed_fields_count,
                        'Field with 12 filters': fields_with_twelve_filters
                        }
                    })

# from django.db import connection
# cursor = connection.cursor()
# cursor.execute('''SELECT count(*) FROM individualfiles''')


