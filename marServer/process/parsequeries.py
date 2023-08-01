from files.models import *

def parseFiles(querySet):
    files = []
    for i in (querySet.all()):
        files.append(i.filepath)

    return files

def parseFinalTiles(querySet, composedBy=True):
    arrProj = []
    querySetList = list(querySet.values())
    for i, l in zip(querySet, querySetList):
        final = dict(l)

        composedBy = i.composedBy.all()
        if composedBy:
            final['composedBy'] = parseIndividuals(composedBy)
        else: pass

        final = dict(final)
        arrProj.append(final)
    return arrProj

def parseProcessed(querySet):
    arrProj = []
    querySetList = list(querySet.values())

    for i, l in zip(querySet, querySetList):
        individual = dict(l)
        individual['masterBiasUsed'] = i.masterBiasUsed.id
        individual['masterFlatUsed'] = i.masterFlatUsed.id
        
        
        individual['sextractorOut'] = parseFiles(i.sextractorOut)
        individual['scampOut'] = parseFiles(i.scampOut)
        individual['swarpOut'] = parseFiles(i.swarpOut)

        

        arrProj.append(individual)

    return arrProj

def parseIndividuals(querySet):
    arrProj = []
    try:
        querySetList = list(querySet.values())
    except:
        querySetList = querySet

    for i, l in zip(querySet, querySetList):
        individual = dict(l)

        sci = i.sci

        if i.superflat:
            sf = SuperFlat.objects.filter(id = i.superflat.id).first()
            individual['superFlatId'] = i.superflat.id
            individual['superFlatPath'] = sf.superFlatPath
            individual['superFlatThumb'] = sf.superFlatThumb
            

        if sci:
            individual['sci'] = parseProcessed(ProcessedSci.objects.filter(id=i.sci.id).all())
            
        individual = dict(individual)
        arrProj.append(individual)
    return arrProj

def parseSci(querySet):
    arrProj = []
    querySetList = list(querySet.values())
    for i, l in zip(querySet, querySetList):
        individual = dict(l)

        sciByfilter = i.sciByFilter.all()
        individual['sciByFilter'] = list(sciByfilter.values())
        individual = dict(individual)
        for key, c in enumerate(sciByfilter):
            individual['sciByFilter'][key].update({"scies": list(c.scies.all().values())})
            individual['sciByFilter'][key].update({"processed": list(c.processed.all().values())})

        arrProj.append(individual)
    return arrProj

def parseFlat(querySet):
    arrProj = []
    querySetList = list(querySet.values())
    for i, l in zip(querySet, querySetList):
        individual = dict(l)

        flatsByFilter = i.flatsByFilter.all()
        individual['flatsByFilter'] = list(flatsByFilter.values())
        individual = dict(individual)
        for key, c in enumerate(flatsByFilter):
            individual['flatsByFilter'][key].update({"flats": list(c.flats.all().values())})

        arrProj.append(individual)
    return arrProj

def parseFlatByFilter(querySet):
    arrProj = []
    querySetList = list(querySet.values())
    for i, l in zip(querySet, querySetList):
        individual = dict(l)

        flats = i.flats.all()
        individual['flats'] = list(flats.values())
        individual = dict(individual)

        arrProj.append(individual)
    return arrProj

def parseSciByFilter(querySet):
    arrProj = []
    querySetList = list(querySet.values())
    for i, l in zip(querySet, querySetList):
        individual = dict(l)
        
        
        scies = i.scies.all()
        processed = i.processed.all()
        final = i.finaltiles.all()
        individual['scies'] = list(scies.values())
        individual['processed'] = list(processed.values())
        individual['finaltiles'] = list(final.values())
        individual = dict(individual)

        arrProj.append(individual)
    return arrProj

def parseBias(querySet):
    arrProj = []
    querySetList = list(querySet.values())
    for i, l in zip(querySet, querySetList):
        individual = dict(l)

        bias = i.bias.all()
        individual['bias'] = list(bias.values())
        individual = dict(individual)

        arrProj.append(individual)
    return arrProj

def parseReduction(querySet):
    arrProj = []
    querySetList = list(querySet.values())

    for i, l in zip(querySet, querySetList):
        individual = dict(l)
        individual['biasBlock'] = parseBias(BiasBlock.objects.filter(id = i.biasBlock.id).all())
        individual['flatsBlock'] = parseFlat(FlatsBlock.objects.filter(id = i.flatsBlock.id).all())
        individual['sciBlock'] = parseSci(SciBlock.objects.filter(id = i.sciBlock.id).all())
        arrProj.append(individual)
    return arrProj
