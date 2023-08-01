from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(IndividualFile)
admin.site.register(BiasBlock)
admin.site.register(FlatByFilter)
admin.site.register(FlatsBlock)
admin.site.register(SciByFilter)
admin.site.register(SciBlock)
admin.site.register(ReductionBlock)
admin.site.register(FinalTiles)
admin.site.register(ProcessedSci)