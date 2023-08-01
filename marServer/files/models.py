from django.db import models

class LockedFields(models.Model):
    field = models.CharField(max_length=30, null=True)
    band = models.CharField(max_length=10, null=True)
    locked_at = models.DateTimeField(auto_now=True, null=True)
    

class File(models.Model):
    filepath = models.CharField(max_length=250, unique=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

# Create your models here.
class ProcessedSci(models.Model):
    individual_catalog = models.CharField(max_length=250, null=True)

    masterFlatUsed = models.ForeignKey('FlatByFilter', on_delete=models.DO_NOTHING, null = True)
    masterBiasUsed = models.ForeignKey('BiasBlock', on_delete=models.DO_NOTHING, null = True)

    sciraw = models.ForeignKey('IndividualFile', on_delete=models.DO_NOTHING, null=True)

    sextractorOut = models.ManyToManyField(File, related_name='sextr')
    scampOut = models.ManyToManyField(File, related_name='scamp')
    swarpOut = models.ManyToManyField(File, related_name='swarp')

class AstroCatalogs(models.Model):
    refname = models.CharField(max_length=30, null=True)
    field = models.CharField(max_length=30, null=True)
    file_path = models.CharField(max_length=250, null=True)

class IndividualFile(models.Model):
    obsDate = models.DateTimeField(null=True)
    field = models.CharField(max_length=30, null=True)

    file_type = models.CharField(max_length=10)
    exptime = models.FloatField(null=True)
    band = models.CharField(max_length=10, null = True)

    file_name = models.CharField(max_length=150, unique=True)
    file_path = models.CharField(max_length=250)

    ovfile = models.CharField(max_length=250, null=True)
    ovthumb = models.CharField(max_length=250, null=True)
    thumb = models.CharField(max_length=250, null=True)

    modeavg = models.FloatField(null=True)
    medianavg = models.FloatField(null=True)
    noiseavg = models.FloatField(null=True)
    medianrms = models.FloatField(null=True)
    noiserms = models.FloatField(null=True)
    moonmean = models.FloatField(null=True)

    bpmask = models.CharField(max_length=250, null=True)

    superflat = models.ForeignKey('SuperFlat', on_delete=models.DO_NOTHING, null=True)

    processedDate = models.DateTimeField(auto_now=True, null=True)
    comments = models.CharField(max_length=300, null=True)
    status = models.IntegerField(default=0)
    isvalid = models.IntegerField(default=1)

    raw_sci = models.ForeignKey('self', related_name='raw', on_delete=models.DO_NOTHING, null=True)
    processed = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    sci = models.ForeignKey(ProcessedSci, on_delete=models.CASCADE, null=True) ##Processed sci
    
    crval1 = models.FloatField(null=True)
    crval2 = models.FloatField(null=True)

class FinalTiles(models.Model):
    field = models.CharField(max_length=30, null=True)
    band = models.CharField(max_length=4, null=True)
    file_path = models.CharField(max_length=250, null=True)
    weight_path = models.CharField(max_length=250, null=True)

    file_thumb = models.CharField(max_length=250, null=True)
    weight_thumb = models.CharField(max_length=250, null=True)

    modeavg = models.FloatField(null=True)
    medianavg = models.FloatField(null=True)
    noiseavg = models.FloatField(null=True)
    medianrms = models.FloatField(null=True)
    noiserms = models.FloatField(null=True)

    date = models.DateField(null=True)
    composedBy = models.ManyToManyField(IndividualFile)
    status = models.IntegerField(default=0)
    flag = models.IntegerField(default=-1)

    comments = models.CharField(max_length=300, null=True)
    isvalid = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    crval1 = models.FloatField(null=True)
    crval2 = models.FloatField(null=True)


class BiasBlock(models.Model):
    bias = models.ManyToManyField(IndividualFile)
    masterPath = models.CharField(max_length=150, null=True)
    masterThumb = models.CharField(max_length=250, null=True)

    maskPath = models.CharField(max_length=250, null=True)
    maskThumb = models.CharField(max_length=250, null=True)

    blockStartDate = models.DateField()
    blockEndDate = models.DateField()

    modeavg = models.FloatField(null=True)
    medianavg = models.FloatField(null=True)
    noiseavg = models.FloatField(null=True)
    medianrms = models.FloatField(null=True)
    noiserms = models.FloatField(null=True)

    comments = models.CharField(max_length=300, null=True)
    status = models.IntegerField(default=0)

    isvalid = models.BooleanField(default=True)


class FlatByFilter(models.Model):
    band = models.CharField(max_length=4)
    masterPath = models.CharField(max_length=250, null=True)
    maskPath = models.CharField(max_length=250, null=True)

    masterThumb = models.CharField(max_length=250, null=True)
    maskThumb = models.CharField(max_length=250, null=True)

    blockStartDate = models.DateField()
    blockEndDate = models.DateField()

    modeavg = models.FloatField(null=True)
    medianavg = models.FloatField(null=True)
    noiseavg = models.FloatField(null=True)
    medianrms = models.FloatField(null=True)
    noiserms = models.FloatField(null=True)

    flats = models.ManyToManyField(IndividualFile)

    comments = models.CharField(max_length=300, null=True)
    status = models.IntegerField(default=0)

    isvalid = models.BooleanField(default=True)


class FlatsBlock(models.Model):
    blockStartDate = models.DateField()
    blockEndDate = models.DateField()

    status = models.IntegerField(default=0)
    comments = models.CharField(max_length=300, null=True)
    flatsByFilter = models.ManyToManyField(FlatByFilter)
    isvalid = models.BooleanField(default=True)

class SuperFlat(models.Model):
    blockStartDate = models.DateField(null = True)
    blockEndDate = models.DateField(null = True)
    band = models.CharField(max_length=4, null = True)

    superFlatPath = models.CharField(max_length=250, null=True)
    superFlatThumb = models.CharField(max_length=250, null=True)

    files = models.TextField(null = True)

    status = models.IntegerField(default=0)
    comments = models.CharField(max_length=300, null=True)
    isvalid = models.BooleanField(default=True)

class SciByFilter(models.Model):
    band = models.CharField(max_length=4)
    scies = models.ManyToManyField(IndividualFile, related_name='scies')

    blockStartDate = models.DateField(null=True)
    blockEndDate = models.DateField(null=True)

    processed = models.ManyToManyField(IndividualFile, related_name='sci2proc')
    finaltiles = models.ManyToManyField(FinalTiles, related_name='final')
    
    status = models.IntegerField(default=0)
    comments = models.CharField(max_length=300, null=True)
    isvalid = models.BooleanField(default=True)

class SciBlock(models.Model):
    blockStartDate = models.DateField(null=True)
    blockEndDate = models.DateField(null=True)

    sciByFilter = models.ManyToManyField(SciByFilter)

    status = models.IntegerField(default=0)
    comments = models.CharField(max_length=300, null=True)
    isvalid = models.BooleanField(default=True)


class ReductionBlock(models.Model):
    biasBlock = models.ForeignKey(
        BiasBlock,
        on_delete=models.SET_NULL,
        null=True
    )

    flatsBlock = models.ForeignKey(
        FlatsBlock,
        on_delete = models.SET_NULL,
        null=True
    )

    sciBlock = models.ForeignKey(
        SciBlock,
        on_delete=models.SET_NULL,
        null=True
    )

    startDate = models.DateField()
    endDate = models.DateField()

    status = models.IntegerField(default=0)
    comments = models.CharField(max_length=300, null=True)

class FieldImages(models.Model):
    file_path = models.CharField(max_length=250, null=True)
    field = models.CharField(max_length=30, null=True)
    flag = models.IntegerField(default=-1)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class CurrentConfig(models.Model):
    name = models.CharField(max_length=30, null=True)
    current = models.BooleanField(default=False)
