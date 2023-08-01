import mar
from mar.config import MarManager, resetThreads

from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from files.models import *
from process.parsequeries import *
from files.views import *
from process.process import *

from files.checks import create_12_band_im

from .thread import *
from process.reduction_proc import Reduction_Instance
from datetime import datetime, date

def check_key(key, request):
    if key in request.data:
        return True
    else:
        return False

def get_type(request):
    if 'type' in request.data:
        return request.data['type']
    else:
        return ''

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def get_process(request):
    return Response({'status': True, 'msg': str(Reduction_Instance.status)})

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def scanfolder(request):
    res = scan_folder(request)
    return Response({'status': True, 'msg': res})

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def reset_threads(request):
    Reduction_Instance.set_status()
    Reduction_Instance.queue = []
    resetThreads()
    return Response({'status': True, 'msg': 'reset done'})


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def get_logs(request):
    res = get_logss()
    return Response({'status': True, 'msg': res})


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def clear_logs(request):
    MarManager.clear_logs()
    return Response({'status': True, 'msg': 'cleared'})


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def individualfile(request):
    if 'type' not in request.data:
        return Response({"status": False, "msg": "Request must contain 'type' arg."})

    t = get_type(request)

    valids = 1
    if check_key('valid', request):
        valids = request.data['valid']

    if t == "get":
        if check_key('id', request):
            res = IndividualFile.objects.filter(id=int(request.data['id']), isvalid=valids).all()

        elif check_key('startDate', request) and check_key('endDate', request) and not check_key('contains', request):
            res = IndividualFile.objects.filter(
                obsDate__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).all()
        elif check_key('startDate', request) and check_key('endDate', request) and check_key('contains', request): 
            names = request.data['contains'].replace(' ', '').split(',')
            res = []
            for name in names:
                tmp = IndividualFile.objects.filter(file_name__contains=name, obsDate__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).all()
                res = res + list(tmp.values())
                return Response({"status": True, "msg": res})
        
        elif check_key('contains', request):
            names = request.data['contains'].replace(' ', '').split(',')
            res = []
            for name in names:
                tmp = IndividualFile.objects.filter(file_name__contains=name, isvalid=valids).all()
                res = res + list(tmp.values())
            return Response({"status": True, "msg": res})

        else:
            return Response({"status": False, "msg": "No id or dates found in request"})

        res = parseIndividuals(res)
        return Response({"status": True, "msg": res})

    if t == "validate":
        if check_key("id", request):
            ind = IndividualFile.objects.filter(id=int(request.data['id'])).first()
            ind.isvalid = not ind.isvalid
            ind.save()
            return Response({"status": True, "msg": f"updated value to {ind.isvalid}"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "setstatus":
        if check_key("id", request) and check_key("status", request):
            ind = IndividualFile.objects.filter(id=int(request.data['id'])).first()
            ind.status = int(request.data['status'])
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id or status found in request"})

    if t == "setcomment":
        if check_key("id", request) and check_key("comment", request):
            ind = IndividualFile.objects.filter(id=int(request.data['id'])).first()
            ind.comments = request.data['comment']
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id or comment found in request"})


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def finaltiles(request):
    if 'type' not in request.data:
        return Response({"status": False, "msg": "Request must contain 'type' arg."})

    t = get_type(request)

    valids = 1
    if check_key('valid', request):
        valids = request.data['valid']

    if t == "process":
        code = ""
        req_status = 0 
        if "code" in request.data:
            code = request.data["code"]
        if "status" in request.data: 
            req_status = int(request.data["status"])

        if check_key('id', request):
            res = FinalTiles.objects.filter(id = request.data["id"]).first()
            block = SciByFilter.objects.filter(comments = f"{res.field} - {res.band}").first()
            band = res.band
            field = res.field
        elif check_key('field', request) and check_key('band', request):
            block = None
            band = request.data["band"]
            field = request.data["field"]
        else:
            return Response({"status": False, "msg": "No id or field/band found in request"})

        
        if block is None:
            block = SciByFilter(
                band = band,
                comments = f"{field} - {band}"
            )
            block.save()

        block.scies.clear()
        block.processed.clear()

        files = IndividualFile.objects.filter(field = field, band=band, file_type="SCI").all()
        for raw_sci in files:
            block.scies.add(raw_sci)
        
        block.status = 0
        for f in block.scies.all():
            if f.processed is not None:
                if f.processed.status >= req_status: 
                    f.processed.status = req_status
                    f.processed.save()

            if req_status < 1 and f.status > 0:
                f.status = req_status
                f.save()
            f.save()

        block.save()
        
        pscibyfilter(block, code)
        return Response({"status": True, "msg": f"Running scibyfilter block {block.id}"})
    
    if t == "processfield":
        code = ""
        req_status = 0
        if "code" in request.data:
            code = request.data["code"]

        if "field" not in request.data:
            return Response({"status": False, "msg": "No field found in request"})
        field = request.data['field']

        sci_block = SciBlock.objects.filter(comments = f"{field}").first()
        if sci_block is None:
            sci_block = SciBlock(
                comments = f"{field}"
            )
            sci_block.save()

        for band in settings.BANDS:
            block = SciByFilter.objects.filter(comments = f"{field} {band}").first()
            if block is None:
                block = SciByFilter(
                    band = band, 
                    comments = f"{field} {band}"
                )
                block.save()

            block.scies.clear()
            block.processed.clear()

            files = IndividualFile.objects.filter(field = field, band = band, file_type="SCI").all()
            if files is None:
                continue
            if len(files) == 0:
                continue
            for raw_sci in files:
                block.scies.add(raw_sci)

            sci_block.sciByFilter.add(block) 
        
        finals = FinalTiles.objects.filter(field = field).all()
        for final in finals:
            final.status = 0
            final.save()

        if 'status' in request.data:
            req_status = int(request.data['status'])

        for sbf in sci_block.sciByFilter.all():
            if req_status < 1:
                sbf.status = 0
                sbf.save()
        
            for f in sbf.scies.all():
                if f.processed is not None:
                    if f.processed.status >= req_status:
                        f.processed.status = req_status
                    f.processed.save()
                if req_status < 1 and f.status > 0:
                    f.status = 0
                f.save()

            for f in sbf.processed.all():
                if f.status >= req_status:
                    f.status = req_status
                f.save()

        sci_block.save()
        
        process_sci(int(sci_block.id), code)
        return Response({"status": True, "msg": f"Running SciBlock block {sci_block.id}"})

    if t == "setsubstatus":
        if check_key("id", request) and check_key("status", request):
            ind = FinalTiles.objects.filter(id=int(request.data['id'])).first()
            
            for i in ind.composedBy.all():
                i.status = int(request.data['status'])
                i.save()
                raw_sci = i.raw_sci
                if raw_sci is None:
                    raw_sci = IndividualFile.objects.filter(file_name = i.file_name.replace("proc_", "")).first()
                    raw_sci.status = int(request.data['status'])
                raw_sci.save()

            ind.status = int(request.data['status'])
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id or status found in request"})

    if t == "getfields":
        res = FinalTiles.objects.values('field', 'band', 'crval1', 'crval2')
        return Response({"status": True, "msg": res})

    if t == "getshort":
        if check_key('field', request) and check_key('band', request):
            res = FinalTiles.objects.values('id', 'field', 'file_path', 'weight_path', 'file_thumb', 'weight_thumb').filter(
                field=request.data['field'], band=request.data['band'], isvalid=valids).all()
        
            return Response({"status": True, "msg": res})


    if t == "get":
        if check_key('id', request):
            res = FinalTiles.objects.filter(id=int(request.data['id']), isvalid=valids).all()

        elif check_key('startDate', request) and check_key('endDate', request) and check_key('contains', request) and check_key('flag', request): 
            names = request.data['contains'].replace(' ', '').split(',')
            res = []
            flag = int(request.data['flag'])
            for name in names:
                tmp = FinalTiles.objects.filter(field__contains=name, date__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).exclude(flag=-1).extra(where=[f'flag & {flag} = {flag}']).all()
                res = res + list(tmp.values())
            return Response({"status": True, "msg": res})


        elif check_key('startDate', request) and check_key('endDate', request) and check_key('contains', request): 
            names = request.data['contains'].replace(' ', '').split(',')
            res = []
            for name in names:
                tmp = FinalTiles.objects.filter(field__contains=name, date__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).all()
                res = res + list(tmp.values())
            return Response({"status": True, "msg": res})
        

        elif check_key('startDate', request) and check_key('endDate', request):
            res = FinalTiles.objects.filter(
                date__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).all()


        elif check_key('field', request) and check_key('band', request):
            res = FinalTiles.objects.filter(
                field=request.data['field'], band=request.data['band'], isvalid=valids).all()


        elif check_key('field', request):
            res = FinalTiles.objects.filter(
                field=request.data['field'], isvalid=valids).all()

        elif check_key('contains', request):
            names = request.data['contains'].replace(' ', '').split(',')
            res = []
            for name in names:
                tmp = FinalTiles.objects.filter(field__contains=name, isvalid=valids).all()
                res = res + list(tmp.values())
                return Response({"status": True, "msg": res})

        else:
            return Response({"status": False, "msg": "No id or dates found in request"})

        res = parseFinalTiles(res)
        return Response({"status": True, "msg": res})

    if t == "setsuperflat":
        if check_key("field", request) and check_key("band", request) and check_key("superflatid", request):
            field = request.data["field"]
            band = request.data["band"]

            superflat = SuperFlat.objects.filter(id = int(request.data['superflatid'])).first()
            if superflat is None and int(request.data['superflatid']) > 0:
                return Response({"status": False, "msg": "No superflat found"})
            else:
                if band != superflat.band:
                    return Response({"status": False, "msg": "Superflat not found for this band."})
            if int(request.data['superflatid']) < 0:
                superflat = None

            files = IndividualFile.objects.filter(field = field, band = band, file_type="SCI").all()

            for file in files:
                file.superflat = superflat
                file.save()

            procs = IndividualFile.objects.filter(field = field, band = band, file_type="PROCESSED").all()

            for file in procs:
                file.superflat = superflat
                file.save()

            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "validate":
        if check_key("id", request):
            fntl = FinalTiles.objects.filter(id=int(request.data['id'])).first()
            fntl.isvalid = not fntl.isvalid
            fntl.save()
            return Response({"status": True, "msg": f"updated value to {fntl.isvalid}"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "setstatus":
        if check_key("id", request) and check_key("status", request):
            ind = FinalTiles.objects.filter(id=int(request.data['id'])).first()
            ind.status = int(request.data['status'])
            ind.save()

        elif check_key('startDate', request) and check_key('endDate', request) and check_key('contains', request) and check_key('flag', request) and check_key('status', request): 
            names = request.data['contains'].replace(' ', '').split(',')
            flag = int(request.data['flag'])
            for name in names:
                tmp = FinalTiles.objects.filter(field__contains=name, date__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).exclude(flag=-1).extra(where=[f'flag & {flag} = {flag}']).all()
                for ind in tmp:
                    ind.status = int(request.data['status'])
                    ind.save()

        else:
            return Response({"status": False, "msg": "No id or status found in request"})
        
        return Response({"status": True, "msg": "updated values"})
    

    if t == "setcomment":
        if check_key("id", request) and check_key("comment", request):
            ind = FinalTiles.objects.filter(id=int(request.data['id'])).first()
            ind.comments = request.data['comment']
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})
    
    if t == "setflag":
        if check_key("id", request) and check_key("flag", request):
            ind = FinalTiles.objects.filter(id=int(request.data['id'])).first()
            ind.flag = request.data['flag']
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def biasblock(request):
    if 'type' not in request.data:
        return Response({"status": False, "msg": "Request must contain 'type' arg."})

    t = get_type(request)

    valids = 1
    if check_key('valid', request):
        valids = request.data['valid']

    if t == "get":
        if check_key('id', request):
            res = BiasBlock.objects.filter(id=int(request.data['id']), isvalid=valids).all()

        elif check_key('startDate', request) and check_key('endDate', request):
            res = BiasBlock.objects.filter(blockStartDate__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).all()

        else:
            return Response({"status": False, "msg": "No id or dates found in request"})

        res = parseBias(res)
        return Response({"status": True, "msg": res})
    
    if t == "register":
        if not check_key('filepath', request):
            return Response({"status": False, "msg": "No filepath found in request"})
            
        from files.views import is_file_in_directory
        filepath = request.data['filepath']
        if not is_file_in_directory(filepath, settings.ROOTFITS):
            filepath = getFilePathRootFits(filepath)

        try:
            hdu = mar.image.marfits.fromfile(filepath)
        except:
            return Response({"status": False, "msg": "Unable to find file"})
        
        master_type = hdu[0].header["MASTER_TYPE"].strip()
        if master_type != "BIAS":
            return Response({"status": False, "msg": "Incorrect master type."})
        
        startDate = datetime.strptime(hdu[0].header["START_DATE"].strip(), "%Y-%m-%d").date()
        endDate = datetime.strptime(hdu[0].header["END_DATE"].strip(), "%Y-%m-%d").date()
        mask_name = hdu[0].header["MASK_NAME"].strip()
        mask_path = os.path.join(os.path.dirname(filepath), mask_name)
        
        if not os.path.exists(mask_path):
            return Response({"status": False, "msg": f"Could not find {mask_name}"})
        
        bias = BiasBlock(
            blockStartDate = startDate,
            blockEndDate = endDate,
            masterPath = removeRootFitsPath(filepath),
            maskPath = mask_path
        )
        bias.save()
        return Response({"status": True, "msg": f"Created bias block {bias.id}"})

    if t == "create":
        res = createBias(request)
        if isinstance(res, str):
            res = {"status": False, "msg": res}
        else:
            res['status'] = True
        return Response(res)

    if t == "validate":
        if check_key("id", request):
            biasbl = BiasBlock.objects.filter(id=int(request.data['id'])).first()
            biasbl.isvalid = not biasbl.isvalid
            biasbl.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "add":
        if check_key("id", request) and check_key("objid", request):
            biasbl = BiasBlock.objects.filter(id=int(request.data['id'])).first()
            bias = IndividualFile.objects.filter(id=int(request.data['objid'])).first()
            biasbl.bias.add(bias)
            biasbl.save()
            return Response({"status": True, "msg": "added value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "remove":
        if check_key("id", request) and check_key("objid", request):
            biasbl = BiasBlock.objects.filter(id=int(request.data['id'])).first()
            bias = IndividualFile.objects.filter(id=int(request.data['objid'])).first()
            biasbl.bias.remove(bias)
            biasbl.save()
            return Response({"status": True, "msg": "removed value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "setstatus":
        if check_key("id", request) and check_key("status", request):
            biasbl = BiasBlock.objects.filter(id=int(request.data['id'])).first()
            biasbl.status = int(request.data['status'])
            biasbl.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "setsubstatus":
        if check_key("id", request) and check_key("status", request):
            biasbl = BiasBlock.objects.filter(id=int(request.data['id'])).first()
            for f in biasbl.bias.all():
                f.status = int(request.data['status'])
                f.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "setcomment":
        if check_key("id", request) and check_key("comment", request):
            biasbl = BiasBlock.objects.filter(id=int(request.data['id'])).first()
            biasbl.comments = request.data['comment']
            biasbl.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "process":
        if check_key("id", request):
            process_bias(request)
            return Response({"status": True, "msg": "Processing bias block!"})

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def flatblock(request):
    if 'type' not in request.data:
        return Response({"status": False, "msg": "Request must contain 'type' arg."})

    t = get_type(request)

    valids = 1
    if check_key('valid', request):
        valids = request.data['valid']

    if t == "get":
        if check_key('id', request):
            res = FlatsBlock.objects.filter(id=int(request.data['id']), isvalid=valids).all()

        elif check_key('startDate', request) and check_key('endDate', request):
            res = FlatsBlock.objects.filter(
                blockStartDate__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).all()

        else:
            return Response({"status": False, "msg": "No id or dates found in request"})

        res = parseFlat(res)
        return Response({"status": True, "msg": res})

    if t == "create":
        if check_key('startDate', request) and check_key('endDate', request):
            res = createFlat(request)
            if isinstance(res, str):
                res = {"status": False, "msg": res}
            else:
                res['status'] = True
            return Response(res)
        else:
            return Response({"status": False, "msg": "No dates found in request"})

    if t == "validate":
        if check_key("id", request):
            flatbl = FlatsBlock.objects.filter(id=int(request.data['id'])).first()
            flatbl.isvalid = not flatbl.isvalid

            for i in flatbl.flatsByFilter.all():
                i.isvalid = not i.isvalid
                i.save()

            flatbl.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "add":
        if check_key("id", request) and check_key("objid", request):
            flatbl = FlatsBlock.objects.filter(id=int(request.data['id'])).first()

            flat = FlatByFilter.objects.filter(id=int(request.data['objid'])).first()
            flatbl.flatsByFilter.add(flat)
            flatbl.save()
            return Response({"status": True, "msg": "added value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "remove":
        if check_key("id", request) and check_key("objid", request):
            flatbl = FlatsBlock.objects.filter(id=int(request.data['id'])).first()

            flat = FlatByFilter.objects.filter(id=int(request.data['objid'])).first()
            flatbl.flatsByFilter.remove(flat)
            flatbl.save()
            return Response({"status": True, "msg": "removed value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "setstatus":
        if check_key("id", request) and check_key("status", request):
            ind = FlatsBlock.objects.filter(id=int(request.data['id'])).first()
            ind.status = int(request.data['status'])
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "setsubstatus":
        if check_key("id", request) and check_key("status", request):
            ind = FlatsBlock.objects.filter(id=int(request.data['id'])).first()

            for f in ind.flatsByFilter.all():
                f.status = int(request.data['status'])
                f.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "setcomment":
        if check_key("id", request) and check_key("comment", request):
            ind = FlatsBlock.objects.filter(id=int(request.data['id'])).first()
            ind.comments = request.data['comment']
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "process":
        if check_key("id", request):
            process_flat(request)
            return Response({"status": True, "msg": "Processing bias block!"})


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def flatbyfilter(request):
    if 'type' not in request.data:
        return Response({"status": False, "msg": "Request must contain 'type' arg."})

    t = get_type(request)

    valids = 1
    if check_key('valid', request):
        valids = request.data['valid']

    if t == "get":
        if check_key('id', request):
            res = FlatByFilter.objects.filter(id=int(request.data['id']), isvalid=valids).all()

        elif check_key('startDate', request) and check_key('endDate', request):
            res = FlatByFilter.objects.filter(
                blockStartDate__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).all()

        else:
            return Response({"status": False, "msg": "No id or dates found in request"})

        res = parseFlatByFilter(res)
        return Response({"status": True, "msg": res})
    
    if t == "register":
        if not check_key('filepath', request):
            return Response({"status": False, "msg": "No filepath found in request"})
            
        from files.views import is_file_in_directory
        filepath = request.data['filepath']
        if not is_file_in_directory(filepath, settings.ROOTFITS):
            filepath = getFilePathRootFits(filepath)

        try:
            hdu = mar.image.marfits.fromfile(filepath)
        except:
            return Response({"status": False, "msg": "Unable to find file"})
        
        master_type = hdu[0].header["MASTER_TYPE"].strip()
        if master_type != "FLAT":
            return Response({"status": False, "msg": "Incorrect master type."})
        
        startDate = datetime.strptime(hdu[0].header["START_DATE"].strip(), "%Y-%m-%d").date()
        endDate = datetime.strptime(hdu[0].header["END_DATE"].strip(), "%Y-%m-%d").date()
        mask_name = hdu[0].header["MASK_NAME"].strip()
        band = hdu[0].header["BAND"].strip()
        mask_path = os.path.join(os.path.dirname(filepath), mask_name)
        
        if not os.path.exists(mask_path):
            return Response({"status": False, "msg": f"Could not find {mask_name}"})
        
        flatf = FlatByFilter(
            blockStartDate = startDate,
            blockEndDate = endDate,
            masterPath = removeRootFitsPath(filepath),
            maskPath = mask_path,
            band = band
        )
        flatf.save()
        return Response({"status": True, "msg": f"Created flatbyfilter block {flatf.id}"})

    if t == "create":
        if check_key('startDate', request) and check_key('endDate', request) and check_key('band', request):
            res = createFlatByFilter(request)
            res['status'] = True
            return Response(res)
        else:
            return Response({"status": False, "msg": "No dates or band found in request"})

    if t == "validate":
        if check_key("id", request):
            flatbl = FlatByFilter.objects.filter(id=int(request.data['id'])).first()
            flatbl.isvalid = not flatbl.isvalid
            flatbl.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "add":
        if check_key("id", request) and check_key("objid", request):
            flatbl = FlatByFilter.objects.filter(id=int(request.data['id'])).first()

            flat = IndividualFile.objects.filter(id=int(request.data['objid']), band=flatbl.band, file_type='FLAT').first()
            flatbl.flats.add(flat)
            flatbl.save()
            return Response({"status": True, "msg": "added value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "remove":
        if check_key("id", request) and check_key("objid", request):
            flatbl = FlatByFilter.objects.filter(id=int(request.data['id'])).first()

            flat = IndividualFile.objects.filter(id=int(request.data['objid'])).first()
            flatbl.flats.remove(flat)
            flatbl.save()
            return Response({"status": True, "msg": "removed value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "setstatus":
        if check_key("id", request) and check_key("status", request):
            ind = FlatByFilter.objects.filter(id=int(request.data['id'])).first()
            ind.status = int(request.data['status'])
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "setsubstatus":
        if check_key("id", request) and check_key("status", request):
            ind = FlatByFilter.objects.filter(id=int(request.data['id'])).first()

            for f in ind.flats.all():
                f.status = int(request.data['status'])
                f.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})


    if t == "setcomment":
        if check_key("id", request) and check_key("comment", request):
            ind = FlatByFilter.objects.filter(id=int(request.data['id'])).first()
            ind.comments = request.data['comment']
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "process":
        code = None
        if (check_key("code", request)):
            code = request.data['code']
        if check_key("id", request):
            bl = FlatByFilter.objects.filter(id=int(request.data['id'])).first()
            pflatbyfilter(bl, code)
            return Response({"status": True, "msg": f"running flatbyfilter block {bl.id}"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def sciblock(request):
    if 'type' not in request.data:
        return Response({"status": False, "msg": "Request must contain 'type' arg."})

    t = get_type(request)
    if t == "get":
        
        valids = 1
        if check_key('valid', request):
            valids = request.data['valid']

        if check_key('id', request):
            res = SciBlock.objects.filter(id=int(request.data['id']), isvalid=valids).all()

        elif check_key('startDate', request) and check_key('endDate', request):
            res = SciBlock.objects.filter(
                blockStartDate__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).all()

        else:
            return Response({"status": False, "msg": "No id or dates found in request"})

        res = parseSci(res)
        return Response({"status": True, "msg": res})

    if t == "create":
        if check_key('startDate', request) and check_key('endDate', request):
            res = createSci(request)
            res['status'] = True
            return Response(res)
        else:
            return Response({"status": False, "msg": "No dates or band found in request"})


    if t == "validate":
        if check_key("id", request):
            scibl = SciBlock.objects.filter(id=int(request.data['id'])).first()
            scibl.isvalid = not scibl.isvalid

            for i in scibl.sciByFilter.all():
                i.isvalid = not i.isvalid
                i.save()

            scibl.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "add":
        if check_key("id", request) and check_key("objid", request):
            scibl = SciBlock.objects.filter(id=int(request.data['id'])).first()

            sci = SciByFilter.objects.filter(id=int(request.data['objid'])).first()
            scibl.sciByFilter.add(sci)
            scibl.save()
            return Response({"status": True, "msg": "added value."})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "remove":
        if check_key("id", request) and check_key("objid", request):
            scibl = SciBlock.objects.filter(id=int(request.data['id'])).first()
            sci = SciByFilter.objects.filter(id=int(request.data['objid'])).first()
            scibl.sciByFilter.remove(sci)
            scibl.save()
            return Response({"status": True, "msg": "removed value."})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "setstatus":
        if check_key("id", request) and check_key("status", request):
            ind = SciBlock.objects.filter(id=int(request.data['id'])).first()
            ind.status = int(request.data['status'])
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "setsubstatus":
        if check_key("id", request) and check_key("status", request):
            sci = SciBlock.objects.filter(id=int(request.data['id'])).first()

            for sbf in sci.sciByFilter.all():
                sbf.status = int(request.data['status'])
                sbf.save()
            
                for f in sbf.scies.all():
                    f.status = int(request.data['status'])
                    f.save()

                for f in sbf.processed.all():
                    f.status = int(request.data['status'])
                    f.save()

            return Response({"status": True, "msg": "updated values"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "setcomment":
        if check_key("id", request) and check_key("comment", request):
            ind = SciBlock.objects.filter(id=int(request.data['id'])).first()
            ind.comments = request.data['comment']
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "process":
        if check_key("id", request):
            if 'id' not in request.data:
                return Response({"status": False, "msg": "Request must contain 'id' arg."})
            code = ""
            if 'code' in request.data:
                code = request.data['code']

            process_sci(request.data['id'], code)
            return Response({"status": True, "msg": "Processing sci block!"})

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def scibyfilter(request):
    if 'type' not in request.data:
        return Response({"status": False, "msg": "Request must contain 'type' arg."})

    t = get_type(request)

    valids = 1
    if check_key('valid', request):
        valids = request.data['valid']

    if t == "get":
        if check_key('id', request):
            res = SciByFilter.objects.filter(id=int(request.data['id']), isvalid=valids).all()

        elif check_key('startDate', request) and check_key('endDate', request):
            res = SciByFilter.objects.filter(
                blockStartDate__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).all()
        else:
            return Response({"status": False, "msg": "No id or dates found in request"})

        res = parseSciByFilter(res)
        return Response({"status": True, "msg": res})

    if t == "create":
        if check_key('startDate', request) and check_key('endDate', request) and check_key('band', request):
            res = createSciByFilter(request)
            res['status'] = True
            return Response(res)
        else:
            return Response({"status": False, "msg": "No dates or band found in request"})

    if t == "validate":
        if check_key("id", request):
            scibl = SciByFilter.objects.filter(id=int(request.data['id'])).first()
            scibl.isvalid = not scibl.isvalid
            scibl.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})
    
    if t == "setsuperflat":
        if check_key("id", request) and check_key("superflatid", request):

            superflat = SuperFlat.objects.filter(id = int(request.data['superflatid'])).first()
            if superflat is None and int(request.data['superflatid']) > 0:
                return Response({"status": False, "msg": "No superflat found"})
            if int(request.data['superflatid']) < 0:
                superflat = None

            ind = SciByFilter.objects.filter(id=int(request.data['id'])).first()
            
            for f in ind.scies.all():
                f.superflat = superflat
                f.save()

            for f in ind.processed.all():
                f.superflat = superflat
                f.save()


            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "add":
        if check_key("id", request) and check_key("objid", request):
            scibl = SciByFilter.objects.filter(id=int(request.data['id'])).first()
            sci = IndividualFile.objects.filter(id=int(request.data['objid']), band=scibl.band, file_type='SCI').first()
            scibl.scies.add(sci)
            scibl.save()
            return Response({"status": True, "msg": "added value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "remove":
        if check_key("id", request) and check_key("objid", request):
            scibl = SciByFilter.objects.filter(id=int(request.data['id'])).first()
            sci = IndividualFile.objects.filter(id=int(request.data['objid'])).first()
            scibl.scies.remove(sci)
            scibl.processed.remove(sci.processed.id)
            scibl.save()
            
            return Response({"status": True, "msg": "removed value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "setstatus":
        if check_key("id", request) and check_key("status", request):
            ind = SciByFilter.objects.filter(id=int(request.data['id'])).first()
            ind.status = int(request.data['status'])
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "setsubstatus":
        if check_key("id", request) and check_key("status", request):
            ind = SciByFilter.objects.filter(id=int(request.data['id'])).first()
            
            for f in ind.scies.all():
                f.status = int(request.data['status'])
                f.save()

            for f in ind.processed.all():
                f.status = int(request.data['status'])
                f.save()

            return Response({"status": True, "msg": "updated values"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})


    if t == "setcomment":
        if check_key("id", request) and check_key("comment", request):
            ind = SciByFilter.objects.filter(id=int(request.data['id'])).first()
            ind.comments = request.data['comment']
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "process":
        code = None
        if (check_key("code", request)):
            code = request.data['code']
        if check_key("id", request):
            bl = SciByFilter.objects.filter(id=int(request.data['id'])).first()
            pscibyfilter(bl, code)
            return Response({"status": True, "msg": f"running scibyfilter block {bl.id}"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def fieldimages(request):
    if 'type' not in request.data:
        return Response({"status": False, "msg": "Request must contain 'type' arg."})

    t = get_type(request)

    if t == "get":
        if check_key('id', request):
            res = FieldImages.objects.filter(id=int(request.data['id'])).all()

        elif check_key('field', request):
            res = FieldImages.objects.filter(field=request.data['field']).all()

        elif check_key('contains', request):
            names = request.data['contains'].strip().split(',')
            res = []
            for name in names:
                res += list(FieldImages.objects.filter(field__contains=name).all().values())
            
            return Response({"status": "true", "msg": res})
        else:
            return Response({"status": False, "msg": "No id or dates found in request"})

        return Response({"status": True, "msg": res.values()})
    
    if t == "process":
        
        field = None
        if check_key('id', request):
            res = FieldImages.objects.filter(id=int(request.data['id'])).first()
            field = res.field
        elif check_key('field', request):
            field = request.data['field']

        if field is None:
            return Response({"status": False, "msg": "No id or field found."})

        MarManager.submit(create_12_band_im, field, True)
        return Response({"status": True, "msg": "Processing field. Check logs."})

    if t == "setflag":
        if check_key("id", request) and check_key("flag", request):
            ind = FieldImages.objects.filter(id=int(request.data['id'])).first()
            ind.flag = request.data['flag']
            ind.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id or flag found in request"})

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated, ))
def superflatblock(request):
    if 'type' not in request.data:
        return Response({"status": False, "msg": "Request must contain 'type' arg."})

    t = get_type(request)

    valids = 1
    if check_key('valid', request):
        valids = request.data['valid']

    if t == "get":
        if check_key('id', request):
            res = SuperFlat.objects.filter(id=int(request.data['id']), isvalid=valids).all()

        elif check_key('startDate', request) and check_key('endDate', request):
            res = SuperFlat.objects.filter(blockStartDate__range=[request.data['startDate'], request.data['endDate']], isvalid=valids).all()

        else:
            return Response({"status": False, "msg": "No id or dates found in request"})

        res = res.values()
        return Response({"status": True, "msg": res})
    
    if t == "register":
        if not check_key('filepath', request):
            return Response({"status": False, "msg": "No filepath found in request"})
            
        from files.views import is_file_in_directory
        filepath = request.data['filepath']
        if not is_file_in_directory(filepath, settings.ROOTFITS):
            filepath = getFilePathRootFits(filepath)

        try:
            hdu = mar.image.marfits.fromfile(filepath)
        except:
            return Response({"status": False, "msg": "Unable to find file"})
        
        master_type = hdu[0].header["MASTER_TYPE"].strip()
        if master_type != "FRINGE":
            return Response({"status": False, "msg": "Incorrect master type."})
        
        startDate = datetime.strptime(hdu[0].header["START_DATE"].strip(), "%Y-%m-%d").date()
        endDate = datetime.strptime(hdu[0].header["END_DATE"].strip(), "%Y-%m-%d").date()
        band = hdu[0].header["BAND"].strip()

        superf = SuperFlat(
            blockStartDate = startDate,
            blockEndDate = endDate,
            superFlatPath = removeRootFitsPath(filepath),
            band = band
        )
        superf.save()
        return Response({"status": True, "msg": f"Created superflat block {superf.id}"})

    if t == "validate":
        if check_key("id", request):
            superflat = SuperFlat.objects.filter(id=int(request.data['id'])).first()
            superflat.isvalid = not superflat.isvalid
            superflat.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id found in request"})

    if t == "setstatus":
        if check_key("id", request) and check_key("status", request):
            superflat = SuperFlat.objects.filter(id=int(request.data['id'])).first()
            superflat.status = int(request.data['status'])
            superflat.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "setsubstatus":
        if check_key("id", request) and check_key("status", request):
            superflat = SuperFlat.objects.filter(id=int(request.data['id'])).first()
            for f in superflat.bias.all():
                f.status = int(request.data['status'])
                f.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})

    if t == "setcomment":
        if check_key("id", request) and check_key("comment", request):
            superflat = SuperFlat.objects.filter(id=int(request.data['id'])).first()
            superflat.comments = request.data['comment']
            superflat.save()
            return Response({"status": True, "msg": "updated value"})
        else:
            return Response({"status": False, "msg": "No id nor status found in request"})
