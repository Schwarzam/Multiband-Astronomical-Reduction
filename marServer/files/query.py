from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated

from django.db import connection
from .models import FinalTiles
import pandas as pd

from files.trilogy import Trilogy
from files.auxs import get_master_path, removeRootFitsPath, getFilePathRootFits
import os

from django.conf import settings

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def rawQuery(request):
    if 'query' not in request.data:
        return Response({"error": "Must fill query"})

    try:
        with connection.cursor() as cursor:
            cursor.execute(request.data["query"])
            t = dictfetchall(cursor)

        df = pd.DataFrame(t)
        tmp = os.path.join(settings.ROOTFITS, "TMP")
        df.to_csv(os.path.join(tmp, "query_result.csv"))
        
        return Response({'msg': removeRootFitsPath(os.path.join(tmp, "query_result.csv")), 'query': request.data["query"]})

    except:
        return Response({'error': 'Error running query'})


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def get_trilogy_image(request):
    if 'field' not in request.data:
        return Response({"error": "Must fill field"})

    try:
        res = FinalTiles.objects.filter(field=request.data["field"]).all()

        df = pd.DataFrame(list(res.values()))

        bands = ["G", "R", "I", "Z", "U", "F378", "F395", "F410", "F430", "F515", "F660", "F861"]
        bands.sort()
        
        bs = list(df["band"].unique())
        bs.sort()

        if (bs == bands):
            print("Found all bands.")
        else:
            print("Missing bands.")
            return Response({'error': 'Missing bands'})
        
        pathdict = {}
        for band in bands:
            pathdict[band] = getFilePathRootFits(df[df["band"] == band]["file_path"].values[0])

        if 'request_order' in request.data:
            request_order = request.data['request_order']
        else:
            request_order = 'R,I,F861,Z-G,F515,F660-U,F378,F395,F410,F430'
        
        tmp = get_master_path("TMP")
        t = Trilogy(pathdict, request_order)
        

        tilepath = os.path.join(get_master_path("TILES"), request.data['field'])
        final_path = os.path.join(tilepath, f"{request.data['field']}.png")
        t.save(final_path)

        return Response({'msg': removeRootFitsPath(final_path)})
    except:
        return Response({'error': 'Error creating image'})