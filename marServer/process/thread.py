import threading
from .reduction_proc import *

from mar.config import MarManager

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def get_logs(request):
    logs = MarManager.get_logs()
    nlogs = {}

    for i in logs:
        file = open(logs[i], 'r')
        nlogs[i] = file.read().splitlines()

        file.close()


    return Response(nlogs)

def get_logss():

    nlogs = {}

    file = open(MarManager.log, 'r')
    nlogs['main'] = file.read().split('\n')[::-1]

    file.close()

    return nlogs
