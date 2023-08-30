import os

import mar
from shutil import copyfile
from files.models import *
from django.conf import settings

from files.views import addFile
from astropy.io import fits
from astropy.table import Table

import astropy
import numpy as np

from files.auxs import *
from mar.config import MarManager
from mar.wrappers import make_thumb
from mar.utilities.timer import timer_t0, timer_t1
from mar.utilities.headerops import remove_keywords_with_patterns

from astropy.io import fits  

from datetime import datetime, timedelta
import time

from mar import env
from threading import Lock


import shutil

try:
    import lacosmicx
    from lacosmicx import apply_mask
except:
    MarManager.WARNING('Couldnt import C apply mask.')
    from mar.reduction import py_apply_mask as apply_mask

#if mar.env.marConf['config']['USE_GPU']:
#    from mar.reduction import py_apply_mask_gpu as apply_mask
#    MarManager.INFO('Using gpu mask applyer.')


global ReductionClass

#Code for operations -- 
# ov - overscan
# sf - subtract fringe
# co - coadded
# am - astrometry
# mc - maskcorrection 

# ov sf co am mc

lock = Lock()

class ProcessReduction:
    def __init__(self):
        self.status = "Available"
        #{'function': '', 'date': '', 'block': ''}
        self.queue = []
        self.code = 'ov sf co am mc'

        self.queueid = 0 
        clear_TMP()

    def getQueue(self):
        return self.queue

    def getFirstQueue(self):
        if len(self.queue) > 0:
            return self.queue[0]
        else:
            return None
    
    def addTask(self, function, block=None, code=None):
        self.queue.append({'id': self.queueid , 'function': str(function), 'block': block, 'code': code})
        self.queueid += 1

    def removeTask(self, id):
        for i in self.queue:
            if i['id'] == int(id):
                self.queue.remove(i)

    def walkQueue(self):
        self.queue = self.queue[1:]

    def set_block_id(self, ident):
        if self.lockProc == False:
            self.id = ident
    
    def set_code(self, code = 'ov im sf co am mc'):
        self.code = code

    def set_status(self, status="Available"):
        self.status = status

    def get_statuc(self):
        return self.status


    def master_bias(self, biasBlockID = None, code=None):
        '''
        Function to process BIAS, overscan, masterBIAS, badpixel mask
        This function uses the mar package in the order to work with S-PLUS
        '''
        self.set_status("Processing BIAS RAW")
        timer_t0.reset()

        if code is None or code.strip() == '':
            code = self.code

        if biasBlockID is None:
            block = ReductionBlock.objects.filter(id = self.id).first()
            bias_block = block.biasBlock
        else:
            bias_block = BiasBlock.objects.filter(id = biasBlockID).first()

        if int(bias_block.status) == 1:
            MarManager.INFO("BIAS Block already processed")
            self.set_status()
            return

        files = []
        for item in bias_block.bias.filter(isvalid=1):
            files.append(getFilePathRootFits(item.file_path))
        
        mbias = mar.reduction.MasterBias(files=files, outdir=get_master_path("TMP"), perAmp=False)
        self.set_status("Running Overscan on BIAS")
        mbias.run_overscan(genThumb=True)

        self.set_status("Saving stats of images.")

        for item in bias_block.bias.filter(isvalid=1):
            ovscfile = "OVSC_" + get_filename(item.file_path).replace(".fz", "")

            hdu = fits.open(os.path.join(get_master_path("TMP"), ovscfile))
            x = mar.image.ComputeStats(hdu)
            x.calcallstats()

            item.modeavg = round(x.modeavg, 6)
            item.medianavg = round(x.medianavg, 6)
            item.noiseavg = round(x.noiseavg, 6)
            item.medianrms = round(x.medianrms, 6)
            item.noiserms = round(x.noiserms, 6)

            ovthumbDefinitive = move_file(os.path.join(get_master_path("TMP"), ovscfile.replace(".fits", ".png")), item.obsDate, "THUMBS")
            ovthumbDefinitive = removeRootFitsPath(ovthumbDefinitive)
            item.ovthumb = ovthumbDefinitive

            item.save()

        self.set_status("Producing MasterBias")
        mbias.run_imcombine()

        mbias.getBPM()
        mbias.del_procfiles()

        sD = bias_block.blockStartDate
        eD = bias_block.blockEndDate

        maskPath = generateName("BIAS", "hotmask", sD, eD)
        masterPath = generateName("BIAS", "masterbias", sD, eD)
        mbias.bpmask.writeto(maskPath, compress=False, overwrite=True)
        mbias.hdu.writeto(masterPath, compress=False, overwrite=True)

        # Create thumbs
        thumbFolder = os.path.join(get_master_path("THUMBS"), "MASTERS", "BIAS")
        check_path(thumbFolder)
        make_thumb(maskPath, os.path.join(thumbFolder, get_filename(maskPath, strip=True) + '.png'))
        make_thumb(masterPath, os.path.join(thumbFolder, get_filename(masterPath, strip=True) + '.png'))

        bias_block.maskThumb = removeRootFitsPath(os.path.join(thumbFolder, get_filename(maskPath, strip=True) + '.png'))
        bias_block.masterThumb = removeRootFitsPath(os.path.join(thumbFolder, get_filename(masterPath, strip=True) + '.png'))

        bias_block.masterPath = removeRootFitsPath(masterPath)
        bias_block.maskPath = removeRootFitsPath(maskPath)
        bias_block.status = 1
        bias_block.save()

        self.set_status('Calculating Stats on biasbl')
        hdu = fits.open(getFilePathRootFits(bias_block.masterPath), mode="update")
        hdu[0].header["MASTER_TYPE"] = "BIAS"
        hdu[0].header["START_DATE"] = bias_block.blockStartDate.strftime("%Y-%m-%d")
        hdu[0].header["END_DATE"] = bias_block.blockEndDate.strftime("%Y-%m-%d")
        hdu[0].header["MASK_NAME"] = os.path.basename(maskPath)

        hdu.flush()
        
        x = mar.image.ComputeStats(hdu)
        x.calcallstats()

        bias_block.modeavg = round(x.modeavg, 6)
        bias_block.medianavg = round(x.medianavg, 6)
        bias_block.noiseavg = round(x.noiseavg, 6)
        bias_block.medianrms = round(x.medianrms, 6)
        bias_block.noiserms = round(x.noiserms, 6)
        bias_block.save()

        MarManager.TIME(f"BIAS Block of {len(bias_block.bias.filter(isvalid=1))} images ran in {timer_t0.minutes()} minutes")
        self.set_status()

        clear_TMP()


    def master_flat(self, flatBlockID = None, code=None):      
        '''
        Function to process Flats, overscan, master and badpixel mask   
        '''
        if code is None or code.strip() == '':
            code = self.code

        self.set_status("Processing FLAT RAW")
        if flatBlockID is None:
            block = ReductionBlock.objects.filter(id = self.id).first()
            flat_block = block.flatsBlock
        else:
            flat_block = FlatsBlock.objects.filter(id = flatBlockID).first()

        filterBlocks = flat_block.flatsByFilter.all()

        for bl in filterBlocks:
            self.processFlatByFilter(bl, code=code)

    def processFlatByFilter(self, flat_by_filter, code=None):

        timer_t0.reset()
        if int(flat_by_filter.status) == 1:
            MarManager.INFO("Flat Block already processed")
            self.set_status()
            return

        self.set_status(f"Processing FLAT {flat_by_filter.band}")
        if code is None or code.strip() == '':
            code = self.code

        files = []
        bias_to_use = {}
        for item in flat_by_filter.flats.filter(isvalid=1):
            try:
                biasMaster = BiasBlock.objects.filter(blockStartDate__lte=item.obsDate, blockEndDate__gte=item.obsDate, status=1, isvalid=1).values('masterPath').first()['masterPath']
            except:
                biasMaster = None
            if biasMaster is None:
                MarManager.CRITICAL("No valid Master bias for date " + item.obsDate.date().__str__() + ". There could be more dates without masters done.")
                self.set_status()
                return
            if biasMaster not in bias_to_use:
                bias_to_use[biasMaster] = []
            bias_to_use[biasMaster].append(getFilePathRootFits(getFilePathRootFits(item.file_path)))
            files.append(getFilePathRootFits(item.file_path))

        if len(files) < 2:
            MarManager.CRITICAL("Only " + str(len(files)) + " for band " + str(flat_by_filter.band))
            self.set_status()
            return

        self.set_status(f"Processing FLAT {flat_by_filter.band} overscan")
        for masterPath in bias_to_use:
            mflat = mar.reduction.MasterFlat(files=bias_to_use[masterPath], outdir=get_master_path("TMP"))
            mflat.run_overscan(masterBias=getFilePathRootFits(masterPath), genThumb=True, subtract_bias=True)

        mflat = mar.reduction.MasterFlat(files=files, outdir=get_master_path("TMP"))
        self.set_status(f"Processing FLAT {flat_by_filter.band} image stats")
        
        for item in flat_by_filter.flats.filter(isvalid=1):
            ovscfile = "OVSC__" + get_filename(item.file_path).replace(".fz", "")

            hdu = fits.open(os.path.join(get_master_path("TMP"), ovscfile))
            x = mar.image.ComputeStats(hdu)
            x.calcallstats()
            
            item.modeavg = round(x.modeavg, 6)
            item.medianavg = round(x.medianavg, 6)
            item.noiseavg = round(x.noiseavg, 6)
            item.medianrms = round(x.medianrms, 6)
            item.noiserms = round(x.noiserms, 6)

            ovthumbDefinitive = move_file(os.path.join(get_master_path("TMP"), ovscfile.replace(".fits", ".png")), item.obsDate, "THUMBS")
            item.ovthumb = removeRootFitsPath(ovthumbDefinitive)

            item.save()
        

        self.set_status(f"Processing FLAT {flat_by_filter.band} MasterFlat")
        mflat.run_imcombine(name = "MasterFlat" + flat_by_filter.band + ".fits")

        sD = flat_by_filter.blockStartDate
        eD = flat_by_filter.blockEndDate

        masterPath = generateName("FLAT", "masterflat", sD, eD, band=flat_by_filter.band)
        maskPath = generateName("FLAT", "coldmask", sD, eD, band=flat_by_filter.band)


        mflat.hdu.writeto(masterPath, compress=False, overwrite=True)

        self.set_status(f"Processing FLAT {flat_by_filter.band} BadPixel Mask")
        mflat.getBPM()
        mflat.bpmask.writeto(maskPath, compress=False, overwrite=True)

        # Create thumbs
        thumbFolder = os.path.join(get_master_path("THUMBS"), "MASTERS", "FLATS")
        check_path(thumbFolder)
        make_thumb(maskPath, os.path.join(thumbFolder, get_filename(maskPath, strip=True) + '.png'))
        make_thumb(masterPath, os.path.join(thumbFolder, get_filename(masterPath, strip=True) + '.png'))

        flat_by_filter.maskThumb = removeRootFitsPath(os.path.join(thumbFolder, get_filename(maskPath, strip=True) + '.png'))
        flat_by_filter.masterThumb = removeRootFitsPath(os.path.join(thumbFolder, get_filename(masterPath, strip=True) + '.png'))

        flat_by_filter.masterPath = removeRootFitsPath(masterPath) 
        flat_by_filter.maskPath = removeRootFitsPath(maskPath)
        flat_by_filter.status = 1
        flat_by_filter.save()

        self.set_status('Calculating Stats on flatf')
        hdu = fits.open(getFilePathRootFits(flat_by_filter.masterPath), mode="update")
        x = mar.image.ComputeStats(hdu)
        x.calcallstats()

        flat_by_filter.modeavg = round(x.modeavg, 6)
        flat_by_filter.medianavg = round(x.medianavg, 6)
        flat_by_filter.noiseavg = round(x.noiseavg, 6)
        flat_by_filter.medianrms = round(x.medianrms, 6)
        flat_by_filter.noiserms = round(x.noiserms, 6)
        flat_by_filter.save()

        hdu[0].header["MASTER_TYPE"] = "FLAT"
        hdu[0].header["START_DATE"] = flat_by_filter.blockStartDate.strftime("%Y-%m-%d")
        hdu[0].header["END_DATE"] = flat_by_filter.blockEndDate.strftime("%Y-%m-%d")
        hdu[0].header["MASK_NAME"] = os.path.basename(maskPath)
        hdu[0].header["BAND"] = flat_by_filter.band

        hdu.flush()

        MarManager.TIME("Master Flat for band " + str(flat_by_filter.band) + " done in " + str(timer_t0.minutes()) + " minutes")
        
        self.set_status()

        clear_TMP()


    def proccess_img(self, sciBlockId=None, code=None):
        if code is None or code.strip() == "":
            code = self.code

        if sciBlockId is None:
            block = ReductionBlock.objects.filter(id = self.id).first()
            sci_block = block.sciBlock
        else:
            sci_block = SciBlock.objects.filter(id = sciBlockId).first()

        filterBlocks = sci_block.sciByFilter.all()
        for bl in filterBlocks:
            self.processSciByFilter(bl, code=code)

            clear_TMP()

    def processSciByFilter(self, sci_by_filter, code=None):
        files = {}
        toOverscan = {}

        if code is None or code.strip() == "":
            code = self.code

        self.set_status(f'Processing sci images on band {sci_by_filter.band}')
        MarManager.INFO(f"Processing sci images on band {sci_by_filter.band} with code: {code}")
        
        timer_t0.reset_all()

        if 'ov' in code:
            for item in sci_by_filter.scies.filter(isvalid=1):

                try: biasMaster = BiasBlock.objects.filter(blockStartDate__lte=item.obsDate, blockEndDate__gte=item.obsDate, status=1, isvalid=1).values('masterPath').first()['masterPath']
                except: biasMaster = None

                try: flatMaster = FlatByFilter.objects.filter(blockStartDate__lte=item.obsDate, blockEndDate__gte=item.obsDate, status=1, isvalid=1, band=item.band).values('masterPath').first()['masterPath']
                except: flatMaster = None
                
                if biasMaster is None:
                    MarManager.CRITICAL("No valid Master bias for date " + item.obsDate.date().__str__() + ". There could be more dates without masters done.")
                    self.set_status()
                    return
                if flatMaster is None:
                    MarManager.CRITICAL("No valid Master flat for date " + item.obsDate.date().__str__() + ". There could be more dates without masters done.")
                    self.set_status()
                    return

                #Create a split symbol to split it later
                master = biasMaster + "--=--" + flatMaster

                if master not in toOverscan:
                    toOverscan[master] = {}

                filepath = generateName("PROCESSED", item.file_path.split('/')[-1].strip('.fz').strip(".fits"), band=sci_by_filter.band)
                check_path(os.path.join(os.path.split(filepath)[0], item.obsDate.date().__str__()))
                files[getFilePathRootFits(item.file_path)] = os.path.join(os.path.split(filepath)[0], item.obsDate.date().__str__(), get_filename(changeFileName(filepath, addBefore="proc_")))
                dbFile = IndividualFile.objects.filter(file_name=get_filename(files[getFilePathRootFits(item.file_path)], strip=True)).first()

                if dbFile is None:
                    dbFile = IndividualFile.objects.filter(file_name=get_filename(files[getFilePathRootFits(item.file_path)] + '.fz', strip=True)).first()

                #if dbFile is None:
                    toOverscan[master][getFilePathRootFits(item.file_path)] = os.path.join(os.path.split(filepath)[0],item.obsDate.date().__str__(),get_filename(changeFileName(filepath, addBefore="proc_")))

                elif dbFile is not None:
                    if dbFile.status < 1 or item.status < 1:
                        toOverscan[master][getFilePathRootFits(item.file_path)] = os.path.join(os.path.split(filepath)[0], item.obsDate.date().__str__(),get_filename(changeFileName(filepath, addBefore="proc_")))
                        if '.fz' in dbFile.file_path:
                            remove(dbFile.file_path)
                            dbFile.file_path = dbFile.file_path.replace('.fz', '')
                            dbFile.save()
                    else:
                        MarManager.INFO(dbFile.file_path + " already overscaned. ")
                        

            if len(files) < 2:
                MarManager.CRITICAL("Only " + str(len(files)) + " for band " + str(sci_by_filter.band))
                #self.set_status()
                #return

            self.set_status("Running overscan on sci images")
            for master in toOverscan:
                if len(toOverscan[master]) > 0:
                    msci = mar.reduction.PrepareSciImages(files=toOverscan[master], outdir=get_master_path("TMP"))
                    masters = master.split("--=--")
                    msci.run_overscan(masterBias=getFilePathRootFits(getFilePathRootFits(masters[0])),
                                    masterFlat=getFilePathRootFits(getFilePathRootFits(masters[1])), genThumb=True, subtract_bias=True)

            for item in sci_by_filter.scies.filter(isvalid=1):
                item.status = 1
            
            #Create instance with all files
            msci = mar.reduction.PrepareSciImages(files=files, outdir=get_master_path("TMP"))

            '''Run through all files to calculate statistics of raw ovsc files and create thumb'''
            self.set_status("Calculating stats on sci images")
            for item in sci_by_filter.scies.filter(isvalid=1):
                try: dbFile = addFile(files[getFilePathRootFits(item.file_path)], tipo = "PROCESSED", retur=True)
                except Exception as e:
                    MarManager.WARN(e)
                    #MarManager.WARN('File will be skipped!')
                    #continue

                dbFile = IndividualFile.objects.filter(file_name=get_filename(files[getFilePathRootFits(item.file_path)], strip=True)).first()
                item.processed = dbFile
                dbFile.raw_sci = item
                dbFile.superflat = item.superflat

                try:
                    if sci_by_filter.processed.filter(file_name = dbFile.file_name).first() is None:
                        sci_by_filter.processed.add(dbFile)
                except Exception as e: MarManager.WARN(e)

                if dbFile.status == 0:
                    dbFile.status = 1
                    dbFile.save()
                elif dbFile.status <= item.status:
                    dbFile.status = item.status
                    dbFile.save()

                sci_by_filter.processed.add(dbFile)

                if item.status < 1:
                    MarManager.INFO("Calculating stats on " + dbFile.file_path)
                    if '.fz' in dbFile.file_path and os.path.exists(getFilePathRootFits(dbFile.file_path.replace('.fz', ''))):
                        MarManager.submit(funpack_db, dbFile, group='funpack')
                    if 'funpack' in MarManager.tasks:
                        MarManager.wait_group_done('funpack')

                    hdu = fits.open(getFilePathRootFits(dbFile.file_path))
                    
                    dbFile.crval1 = round(float(hdu[0].header['CRVAL1']), 6)
                    dbFile.crval2 = round(float(hdu[0].header['CRVAL2']), 6)
                    item.crval1 = round(float(hdu[0].header['CRVAL1']), 6)
                    item.crval2 = round(float(hdu[0].header['CRVAL2']), 6)

                    try: 
                        dbFile.moonmean = round(float(hdu[0].header['MOONMILL']), 6)
                    except Exception as e: 
                        MarManager.WARN("No moonmean in header of " + dbFile.file_name)
                    
                    dbFile.save()

                    x = mar.image.ComputeStats(hdu)
                    x.calcallstats()

                    item.modeavg = round(x.modeavg, 6)
                    item.medianavg = round(x.medianavg, 6)
                    item.noiseavg = round(x.noiseavg, 6)
                    item.medianrms = round(x.medianrms, 6)
                    item.noiserms = round(x.noiserms, 6)

                    newpath = move_file(os.path.join(get_master_path("TMP"), dbFile.file_name + ".png"), dbFile.obsDate, "THUMBS")
                    try: os.rename(newpath, os.path.join(os.path.split(newpath)[0], dbFile.file_name.replace('proc', 'OVSC') + ".png"))
                    except: pass
                    item.ovthumb = removeRootFitsPath(os.path.join(os.path.split(newpath)[0], dbFile.file_name.replace('proc', 'OVSC') + ".png"))

                    item.status = 1
                    item.save()

                sci_by_filter.save()

        marConf = mar.AttributeDict(env.marConf.Fringe)
        superflat_file = None

        if sci_by_filter.band in marConf.FILTERS and 'sf' in code:
            s = sci_by_filter.processed.filter(isvalid=1, status__lt = 2)
            
            needsFringe = False
            files_to_fringe = []

            for file in s:
                MarManager.submit(funpack_db, file, group='funpack')
            if 'funpack' in MarManager.tasks:
                MarManager.wait_group_done('funpack')
                
            for file in s:
                if file.superflat is not None:
                    continue

                superflat = SuperFlat.objects.filter(blockStartDate__lte=file.obsDate, band=file.band, blockEndDate__gte=file.obsDate, isvalid=1).first()

                if not superflat:
                    needsFringe = True
                
                if check_patterns(file.file_name, marConf.FILE_PATTERNS):
                    if not check_patterns(file.file_name, marConf.EXCLUDE_PATTERS):
                        if file.comments:
                            if not 'nf' in file.comments:
                                files_to_fringe.append(getFilePathRootFits(file.file_path))
                        else:
                            files_to_fringe.append(getFilePathRootFits(file.file_path))

            if not needsFringe:
                MarManager.INFO('Fringe found for all files selected')

            if needsFringe:
                self.set_status("Running superflat")
                msci.SuperFlat(files_to_fringe)

                superflat_file = msci.outname
                newfile = os.path.join(get_master_path("FRINGE"), get_filename(generateName(None, f"superflat_{sci_by_filter.band}", sci_by_filter.blockStartDate, sci_by_filter.blockEndDate)))
                copyfile(superflat_file, newfile)
                superflat_file = newfile
                
                make_thumb(superflat_file, superflat_file.replace('.fits', '').replace('.fz', '') + '.png')

                sci_by_filter.save()
                superFlat = SuperFlat(
                    blockStartDate=sci_by_filter.blockStartDate,
                    blockEndDate=sci_by_filter.blockEndDate,
                    superFlatPath=removeRootFitsPath(superflat_file),
                    superFlatThumb=removeRootFitsPath(superflat_file.replace('.fits', '').replace('.fz', '') + '.png'),
                    files=msci.fil,
                    band=sci_by_filter.band
                )
                superFlat.save()

                superflat = mar.image.marfits.fromfile(superflat_file, mode="update")

                superflat[0].header["MASTER_TYPE"] = "FRINGE"
                superflat[0].header["START_DATE"] = sci_by_filter.blockStartDate.strftime("%Y-%m-%d")
                superflat[0].header["END_DATE"] = sci_by_filter.blockEndDate.strftime("%Y-%m-%d")
                superflat[0].header["BAND"] = sci_by_filter.band

                superflat.flush()
                superflat.close()

                del msci, superflat

            waitforgroup = False
            for file in sci_by_filter.processed.filter(isvalid = 1):
                MarManager.INFO(file.file_name + " " + str(file.status))
                if file.status < 2:
                    MarManager.INFO('applying fringe on: ' + file.file_name)
                    if file.superflat is None:
                        spf_obj = SuperFlat.objects.filter(blockStartDate__lte=file.obsDate, blockEndDate__gte=file.obsDate, isvalid=1).first()
                        superflat_file = spf_obj.superFlatPath
                        superflat_file = getFilePathRootFits(superflat_file)
                        file.superflat = spf_obj
                        
                        file.save()
                    else:
                        superflat_file = getFilePathRootFits(file.superflat.superFlatPath)
                
                    MarManager.submit(apply_fringe, file, superflat_file, group="FRINGE")

                    waitforgroup = True
                else:
                    MarManager.INFO('Fringe already applyed on: ' + file.file_name)
            if waitforgroup:
                MarManager.wait_group_done("FRINGE")

        if "mc" in code:
            waitforgroup = False
            self.set_status("Running masks")
            for file in sci_by_filter.processed.filter(isvalid = 1):
                if file.status < 3:
                    biasMask = BiasBlock.objects.filter(blockStartDate__lte=file.obsDate, blockEndDate__gte=file.obsDate, status=1, isvalid=1).values('maskPath').first()['maskPath']
                    flatMask = FlatByFilter.objects.filter(blockStartDate__lte=file.obsDate, blockEndDate__gte=file.obsDate, status=1, isvalid=1, band=file.band).values('maskPath').first()['maskPath']

                    if biasMask is None:
                        MarManager.CRITICAL("No valid HotMask - bias for date " + file.obsDate.date().__str__() + ". There could be more dates without masters done.")
                        return
                    if flatMask is None:
                        MarManager.CRITICAL("No valid ColdMask - flat for date " + file.obsDate.date().__str__() + ". There could be more dates without masters done.")
                        return
                    
                    if mar.env.marConf['config']['USE_GPU']:
                        run_masks(file, getFilePathRootFits(biasMask), getFilePathRootFits(flatMask))
                    else:    
                        MarManager.submit(run_masks, file, getFilePathRootFits(biasMask), getFilePathRootFits(flatMask), group="MASK")
                        waitforgroup = True
                else:
                    MarManager.INFO(file.file_name + ' already mask corrected')
            if(waitforgroup):
                MarManager.wait_group_done("MASK")

        if mar.env.marConf['config']['FPACK_PROCESSED'] and not "am" in code and not "co" in code:
            for file in sci_by_filter.processed.filter(isvalid = 1):
                MarManager.submit(fpack_db, file, group='fpack')
            MarManager.wait_group_done('fpack')

        if "am" in code:
            '''Run astrometry'''
            # for file in sci_by_filter.processed.filter(isvalid = 1):
            #     MarManager.submit(funpack_db, file, group='funpack')
            # if 'funpack' in MarManager.tasks:
            #     MarManager.wait_group_done('funpack')
            #
            self.set_status("Running astrometry")
            run_astro(sci_by_filter.processed.filter(isvalid = 1))

            ''' Run again through all files to calculate new statistics, add catalog and update database'''
            for item in sci_by_filter.processed.filter(isvalid = 1):
                if item.sci is None:
                    proc = ProcessedSci()
                    proc.save()
                else:
                    proc = item.sci

                if item.status == 4: ## Astrometry needs to be corrected
                    path = os.path.join(get_master_path("SCAMP"), item.band, item.file_name)
                    scampfiles = ["distort_1.svg", "astr_interror1d_1.svg", "fgroups_1.svg", "scamp.head"]
                    for plot in scampfiles:
                        if proc.scampOut.filter(filepath=os.path.join(path, plot)) is None:
                            f = File.objects.create(filepath=removeRootFitsPath(os.path.join(path, plot)))
                            proc.scampOut.add(f)

                    proc.masterFlatUsed = FlatByFilter.objects.filter(blockStartDate__lte=item.obsDate, blockEndDate__gte=item.obsDate, status=1, isvalid=1, band=item.band).first()
                    proc.masterBiasUsed = BiasBlock.objects.filter(blockStartDate__lte=item.obsDate, blockEndDate__gte=item.obsDate, status=1, isvalid=1).first()
                    proc.sciraw = IndividualFile.objects.filter(file_name=item.file_name.replace('proc_', '')).first()

                    proc.save()

                    hdu = fits.open(getFilePathRootFits(item.file_path))
                    x = mar.image.ComputeStats(hdu)
                    x.calcallstats()

                    MarManager.INFO(item.file_name + ' modeavg: round(x.modeavg, 6)')
                    item.modeavg = round(x.modeavg, 6)
                    item.medianavg = round(x.medianavg, 6)
                    item.noiseavg = round(x.noiseavg, 6)
                    item.medianrms = round(x.medianrms, 6)
                    item.noiserms = round(x.noiserms, 6)
                    item.sci = proc

                    make_thumb(getFilePathRootFits(item.file_path), getFilePathRootFits(item.file_path).replace('.fits', '').replace('.fz', '') + '.png')
                    item.thumb = removeRootFitsPath(item.file_path).replace('.fits', '').replace('.fz', '') + '.png'
                    item.save()

                    sextr = mar.reduction.SExtractorCatalog(getFilePathRootFits(item.file_path), folder=get_master_path("TMP"))
                    sextr.run()

                    catpath = generateName("TMP", string="catout.param", ext="")  ##Get path of output file Sextractor

                    path = os.path.join(get_master_path("SEXTRACTOR"), item.band, item.file_name)
                    check_path(path)
                    filepath = os.path.join(path, get_filename(catpath))
                    copyfile(catpath, filepath)
                    shutil.copy(filepath, os.path.join(path, item.file_name + ".cat"))

                    configsexpath = generateName("TMP", string="config.sex", ext="")
                    filepath = os.path.join(path, get_filename(configsexpath))
                    copyfile(configsexpath, filepath)

                    try:
                        f = File.objects.create(filepath=removeRootFitsPath(filepath))
                    except:
                        f = File.objects.filter(filepath=removeRootFitsPath(filepath)).first()
                    
                    try:
                        proc.sextractorOut.add(f)
                    except:
                        pass
                    

                    proc.individual_catalog = removeRootFitsPath(os.path.join(path, item.file_name + ".cat"))
                    proc.save()

                    item.status = 5
                    item.save()
                
            if mar.env.marConf['config']['FPACK_PROCESSED'] and not "co" in code:
                for file in sci_by_filter.processed.filter(isvalid = 1):
                    MarManager.submit(fpack_db, file, group='fpack')
                MarManager.wait_group_done('fpack')

        # if "co" in code:
        #     for file in sci_by_filter.processed.filter(isvalid = 1):
        #         MarManager.submit(funpack_db, file, group='funpack')
        #     if 'funpack' in MarManager.tasks:
        #         MarManager.wait_group_done('funpack')
        #
            self.set_status("Running Swarp")
            run_swarp(sci_by_filter.processed.filter(isvalid=1), sci_by_filter)

        if mar.env.marConf['config']['FPACK_PROCESSED']:
            for file in sci_by_filter.processed.filter(isvalid = 1):
                MarManager.submit(fpack_db, file, group='fpack')
            MarManager.wait_group_done('fpack')

        self.set_status()

        MarManager.TIME("Science block for band " + str(sci_by_filter.band) + " done in " + str(timer_t0.minutes()) + " minutes")
        clear_TMP()

def funpack_db(file):
    if ".fz" in file.file_path:
        MarManager.INFO('Funpacking ' + file.file_name)
        c = funpack(getFilePathRootFits(file.file_path), True)
        if c == 0:
            file.file_path = str(file.file_path).replace(".fz", "")
            file.save()
        else:
            MarManager.CRITICAL(f"Error funpacking {file.file_path}")

def fpack_db(file):
    if ".fz" not in file.file_path:
        MarManager.INFO('Fpacking ' + file.file_name)
        c = fpack(getFilePathRootFits(file.file_path), True)
        if c == 0:
            file.file_path = str(file.file_path) + ".fz"
            file.save()
        else:
            MarManager.CRITICAL(f"Error fpacking {file.file_path}")

def apply_fringe(file, superflat):
    if file.status < 2:
        MarManager.INFO(f'Applying Fringe ({file.superflat.id}) correction to {file.file_name}')
        frin = mar.reduction.FringeSubtract(superflat)
        frin.subtractMode()
        frin.ComputeBackgroundfactor(getFilePathRootFits(file.file_path), imdataHDU=0)
        frin.hdu.writeto(getFilePathRootFits(file.file_path), compress=False, overwrite=True)
        file.status = 2
        file.save()
    else:
        MarManager.INFO(file.file_name + 'alread fringe corrected')

def run_masks(file, hotmask, coldmask):
    hotmask = fits.open(hotmask)
    coldmask = fits.open(coldmask)

    file_name = file.file_name
    MarManager.INFO("Running mask for " + file.file_name)
    
    funpack_db(file)

    ## Opening image
    im = mar.image.marfits.fromfile(getFilePathRootFits(file.file_path), usemask = False)

    final_mask = mar.image.MaskArray(
        np.zeros(im[0].data.shape, dtype=np.uint8)
    )

    mask = hotmask[0].data + coldmask[0].data + (im[0].data >= int(mar.env.marConf['Instrument']['SATURATE']))
    mask = mask > 0
    mask = np.ma.masked_array(np.zeros(mask.shape), mask, fill_value=1)
    mask = mask.filled(1).astype(np.uint8)
    
    final_mask.add_mask(mask.astype(np.uint8), 1)

    with lock:
        MarManager.INFO(f"applying first mask {file_name}")
        # important to not pass mask 64 here.  
        im[0].data = apply_mask(np.asarray(im[0].data, dtype=np.float32), mask)
        im.writeto(getFilePathRootFits(file.file_path), compress=False, overwrite=True)
        im = mar.image.marfits.fromfile(getFilePathRootFits(file.file_path), usemask = False)

    del mask 

    ## ------------------------------ ## ------------------------------ ##
    ## Make segmentation mask to not correct pixels where objects were detected
    folder = os.path.join(get_master_path("TMP"), file.file_name)
    check_path(folder)
    sextr = mar.wrappers.SExtr(
        getFilePathRootFits(file.file_path),
        folder=folder,
        catname=file.file_name + "_seg_.cat",
    )
    segmentation_image = os.path.join(folder, file.file_name + "_seg_.fits")
    sextr.config["CHECKIMAGE_TYPE"]['value'] = "SEGMENTATION"
    sextr.config["CHECKIMAGE_NAME"]['value'] = segmentation_image
    sextr.params = [
        'NUMBER',
        'FLAGS'
    ]

    sextr.run()

    table = Table.read(os.path.join(folder, file.file_name + "_seg_.cat"), hdu=2)
    selection = (
		(table["FLAGS"] <= 2)
	)
    table = table[selection]
    segmentation_data = fits.getdata(segmentation_image)
    stars_mask = np.isin(segmentation_data, np.array(table["NUMBER"])).astype("int")
    del segmentation_data

    final_mask.add_mask(
        stars_mask.astype(np.uint8), 64
    )
    del stars_mask
    ## ------------------------------ ## ------------------------------ ##


    with lock:
        MarManager.INFO(f"getting lacosmic {file_name}")
        cosmicMask, im[0].data = mar.reduction.lacosmicx.lacosmicx(np.asarray(im[0].data, dtype=np.float32), final_mask.get_mask([1, 2, 64], binary=True).astype(np.uint8))
        cosmicMask = np.ma.masked_array(np.zeros(cosmicMask.shape), cosmicMask, fill_value=1).filled(1).astype(np.uint8)

        final_mask.add_mask(cosmicMask.astype(np.uint8), 4)

        MarManager.INFO(f"applying cosmic mask to {file_name}")
        #im[0].data = apply_mask(im[0].data, cosmicMask, final_mask.get_mask([64], binary=True).astype(np.uint8))
        im.writeto(getFilePathRootFits(file.file_path), compress=False, overwrite=True)

    
    bpmask = generateName("BPMASK", "bpmask_" + file_name)

    if mar.env.marConf['config']['FILTER_SATELLITE']:
        sat_mask = mar.image.get_satellite_trace(
            image = getFilePathRootFits(file.file_path),
            folder = get_master_path("TMP"),
            catname = file.file_name + "_cat.fits",
            segmentation_name = file.file_name + "_satellite.fits",
        )

        if sat_mask is not None:
            MarManager.INFO("Saving satellite mask.")
            final_mask.add_mask(sat_mask.astype(np.uint8), 8)

    fits.HDUList([fits.PrimaryHDU(data=np.asarray(final_mask, dtype=np.uint8))]).writeto(bpmask, overwrite=True)
    file.bpmask = removeRootFitsPath(bpmask)

    c = fpack(getFilePathRootFits(bpmask), True)
    if c == 0:
        file.bpmask = removeRootFitsPath(str(bpmask) + ".fz")
        file.save()
    else:
        MarManager.CRITICAL(f"Error fpacking {file.bpmask}")

    file.status = 3
    file.save()

    MarManager.INFO("Masked corrected " + file_name)

#Run astrometry
def run_astro(files):
    for f in files:
        MarManager.submit(astro, f, group='astro')
    MarManager.wait_group_done('astro')

def astro(f):
    if f.status < 4:
        MarManager.INFO(f"Running Astrometry for {f.file_name}")
    
        funpack_db(f)

        catalogname = f'{f.file_name.replace(".fits", "")}.catalog'

        tmpfolder = os.path.join(get_master_path("TMP"), f.file_name.replace('.fits', '').replace('.fz', ''))
        check_path(tmpfolder)

        sextr = mar.reduction.SExtractorCatalog(getFilePathRootFits(f.file_path), catname=catalogname, folder=tmpfolder)
        
        # Config found to work on crowded bulge
        sextr.config["DETECT_THRESH"]["value"] = 2
        sextr.config["BACK_FILTERSIZE"]["value"] = 6
        sextr.config["BACK_SIZE"]["value"] = 64
        sextr.config["FILTER"]["value"] = "N"
        sextr.config["PHOT_APERTURES"]["values"] = "(1.4, 20, 90)"

        sextr.run()

        catpath = os.path.join(tmpfolder, catalogname)   ##Get path of output file Sextractor
        
        path = move_file(catpath, f.obsDate, "SEXTRACTOR", f.band)
        shutil.copy(catpath, path)
 
        f.individual_catalog = catpath

        catop = mar.reduction.CatalogOperation(catpath)

        MarManager.INFO(f"Found {len(catop.catalog)} detections.")
        
        catop.stars(distributed = True)
        
        ## TODO: make this item a enviroment config var 
        if len(catop.catalogStars) < 300:
            MarManager.WARN(f"Unable to find more than 300 objets to astrometry, using all objects detected and filtered.")
            #f.isvalid = 2
            #f.save()
            catop.stars(distributed = False)
    
        if len(catop.catalogStars) < 150:
            MarManager.WARN("Unable to find more than 150 objets to astrometry anyway. Passing sextractor catalog without cuts.")
            if len(catop.catalog) > 100:
                catop.stars(distributed=False, do_selection=False)
            else:
                MarManager.CRITICAL("Unable to find more than 100 objets in total. Skipping image.")
                return 

        path = os.path.join(get_master_path("SCAMP"), f.band, f.file_name)
        check_path(path)

        starsCatalog = f'{f.file_name.replace(".fits", "")}.stars.cat'
        starsCatalog = os.path.join(path, starsCatalog)

        MarManager.INFO(f"Found {len(catop.catalogStars)} stars to scamp.")

        catop.saveStarsCatalog(starsCatalog)
 
        scamp = mar.wrappers.RunAstro(catalog=starsCatalog, outdir=tmpfolder, fwhm_seeing=catop.FWHMSEXT)
        
        ref_cat = scamp.config["ASTREF_CATALOG"]["value"]
        outcat_folder = os.path.join(get_master_path("SCAMP"), f.field)    
        check_path(outcat_folder)

        astrocat = AstroCatalogs.objects.filter(field = f.field, refname = ref_cat).first()
        if astrocat is None:
            scamp.config["SAVE_REFCATALOG"]["value"] = "Y"
            scamp.config["REFOUT_CATPATH"]["value"] = outcat_folder
        else:
            MarManager.INFO(f"Using {removeRootFitsPath(astrocat.file_path)} as reference catalog.")
            scamp.config["ASTREF_CATALOG"]["value"] = "FILE"
            scamp.config["ASTREFCAT_NAME"]["value"] = getFilePathRootFits(astrocat.file_path)

        code = scamp.run()

        if astrocat is None and code == 0:
            files = absoluteFilePaths(outcat_folder)
            for file in files:
                if ref_cat in file:
                    astrocat, created = AstroCatalogs.objects.update_or_create(
                        field = f.field,
                        refname = ref_cat,
                        file_path = removeRootFitsPath(file)
                    )
                    MarManager.INFO(f"Saving reference catalog {removeRootFitsPath(astrocat.file_path)}")
                    astrocat.save()
                    break



        if int(code) != 0:
            MarManager.CRITICAL(f"Scamp failed for {f.file_name}")
            return 

        try:
            plot = os.path.join(tmpfolder, "distort_1.svg")
            copyfile(plot, os.path.join(path, "distort_1.svg"))
        except: pass
        try:
            plot = os.path.join(tmpfolder, "astr_interror1d_1.svg")
            copyfile(plot, os.path.join(path, "astr_interror1d_1.svg"))
        except:pass
        try:
            plot = os.path.join(tmpfolder, "fgroups_1.svg")
            copyfile(plot, os.path.join(path, "fgroups_1.svg"))
        except: pass
        try:
            plot = os.path.join(tmpfolder, "scamp.head")
            copyfile(plot, os.path.join(path, "scamp.head"))
        except:pass

        hdu = mar.image.marfits.fromfile(getFilePathRootFits(f.file_path), mode="update")
        
        try:
            head = mar.wrappers.readScampHead(os.path.join(tmpfolder, 'scamp.head'))
            for card in head:
                hdu.setCard(card[0], card[1], card[2])

            hdu.setCard("ASTROMETRY", "SUCCESS", "Astrometry success")
        except:
            hdu.setCard("ASTROMETRY", "FAILED", "Astrometry failed")
        
        MarManager.INFO(f"Updating header of {f.file_name} removing patterns {str(mar.env.marConf['config']['REMOVE_FROM_IND_HEADER'])}")
        hdu[0].header = remove_keywords_with_patterns(hdu[0].header, mar.env.marConf["config"]["REMOVE_FROM_IND_HEADER"])

        hdu.flush()

        f.status = 4
        f.save()
    else:
        MarManager.INFO(f.file_name + ' already astrometry corrected')

def run_swarp(files, sci_by_filter):
    fields_done = []
    fields = {}
    for f in files:
        fi = str(f.field)
        if fi not in fields:
            
            fields.setdefault(fi,[]).append(f)

    MarManager.INFO(f'Fields found {str(list(fields.keys() ))}')
    for field in fields:
        MarManager.submit(swarp, fields[field], sci_by_filter, group="swarp")
    
    MarManager.wait_group_done('swarp')
        
def swarp(fil, sci_by_filter):
    MarManager.INFO(f'Preparing for swarp on {fil[0].field} of {fil[0].obsDate}')
    
    finaltile = FinalTiles.objects.filter(field = fil[0].field, band = fil[0].band, isvalid=1).first()
    if finaltile is None:
        finaltile = FinalTiles()

    fil = list(IndividualFile.objects.filter(field = fil[0].field, isvalid = 1, status=5, band = fil[0].band, file_type="PROCESSED").all())
    if len(fil) == 0 or fil is None:
        MarManager.INFO(f'No files found for field {fil[0].field} of {fil[0].obsDate}')
        return
    
    ## Lock field
    field_lock = LockedFields.objects.filter(field = fil[0].field, band = fil[0].band).first()
    if field_lock is None:
        field_lock = LockedFields()
        field_lock.field = fil[0].field
        field_lock.band = fil[0].band
        field_lock.save()
    else:
        MarManager.INFO(f'Field {fil[0].field} is locked, waiting for field')
        while field_lock is not None:
            time.sleep(10)
            if field_lock.locked_at < datetime.now() - timedelta(minutes=20):
                MarManager.INFO(f'Field {fil[0].field} is locked, but lock is older than 20 minutes, removing lock')
                field_lock.delete()
                field_lock = None
            field_lock = LockedFields.objects.filter(field = fil[0].field, band = fil[0].band).first()


    finaltile.field = fil[0].field
    finaltile.date = fil[0].obsDate
    finaltile.band = fil[0].band
    images = ''
    im_names = []
    exps = []
    
    masks = ''
    masks_names = ''

    resamp = ''
    weights = ''

    crval1_mean = []
    crval2_mean = []

    for item in fil:
        hdu = 0
        if '.fz' in item.file_path:
            hdu = 1
        head = fits.getheader(getFilePathRootFits(item.file_path), hdu=hdu)
        if 'ASTROMETRY' in head:
            if head['ASTROMETRY'] == 'FAILED':
                MarManager.WARN("Not coadding, astrometry failed for " + item.file_name)
                fil.remove(item)

    
    if len(fil) == 0:
        MarManager.CRITICAL("No files to coadd for " + fil[0].field)
        return
    
    for item in fil:
        im_names.append(item.file_name)
    
    try:
        hdu = 0
        if '.fz' in finaltile.file_path:
            hdu = 1
        finaltile_header = fits.getheader(getFilePathRootFits(finaltile.file_path), ext=hdu)
        
        if 'NCOMBINE' in finaltile_header:
            old_n_combine = int(finaltile_header['NCOMBINE'])
            if old_n_combine is None:
                old_n_combine = 0
            old_im_names = []
            for i in range(old_n_combine):
                old_im_names.append(finaltile_header[f'COMB_{i}'])
            
            if sorted(old_im_names) == sorted(im_names) and finaltile.status == 1:
                field_lock.delete()
                MarManager.INFO("Coadded/Swarp already done for " + fil[0].field)
                return
    except Exception as e:
        MarManager.WARN(e)


    for item in fil:
        funpack_db(item)

      
    for item in fil:
        #open masterflat
        flatMaster = FlatByFilter.objects.filter(blockStartDate__lte=item.obsDate, blockEndDate__gte=item.obsDate, status=1, isvalid=1, band=item.band).values('masterPath').first()['masterPath']
        if flatMaster is None:
            MarManager.CRITICAL("No valid Master flat for date " + item.obsDate.date().__str__() + ". There could be more dates without masters done.")
            return

        masterflat = fits.getdata(getFilePathRootFits(flatMaster))
        try:
            ncmode = float(fits.getval(getFilePathRootFits(flatMaster), 'HIERARCH MAR QC NCMODE', 0))
        except:
            ncmode = float(fits.getval(getFilePathRootFits(flatMaster), 'HIERARCH MAR QC NCMODE', 1))

        masterflat /= ncmode

        images = images + ', ' + getFilePathRootFits(item.file_path)
        exps.append(item.exptime) 
 
        MarManager.INFO('Creating swarp weight mask for ' + item.file_name)

        mask_name = os.path.basename(item.bpmask).replace('.fits', '_swarp.fits')
        masks_names = masks_names + ', ' + mask_name

        mask_path = os.path.join(get_master_path("TMP"), mask_name)
        masks = masks + ', ' + mask_path
        
        im = mar.image.marfits.fromfile(
            getFilePathRootFits(item.file_path), 
            usemask = True, 
            maskfile=getFilePathRootFits(item.bpmask)
        )
        
        if '.fz' in item.file_name:
            headerHDU = 1
        else:
            headerHDU = 0

        mask = fits.HDUList([fits.PrimaryHDU(
                data = im.get_mask([1,2, 4, 8], binary=True, inverted=True, dtype='float32'), 
                header = im[headerHDU].header
            )])
        
        crval1_mean.append(float(im[headerHDU].header['CRVAL1']))
        crval2_mean.append(float(im[headerHDU].header['CRVAL2']))

        del im
        
        mask[0].data *= masterflat

        mask.writeto(mask_path, overwrite=True)

        resamp = resamp + ', ' + os.path.join(get_master_path("SWARP"), item.band, item.field, item.file_path.split('/')[-1].replace('.fits', ".resamp.fits"))
        weights = weights + ', ' + os.path.join(get_master_path("SWARP"), item.band, item.field, item.file_path.split('/')[-1].replace('.fits', ".resamp.weight.fits"))

    MarManager.DEBUG(f'Images found {images}')
    MarManager.DEBUG(f'Masks found {masks}')
    
    reference = IndividualFile.objects.filter(field=fil[0].field, band='R').first()
    if reference is not None:
        header = fits.getheader(getFilePathRootFits(reference.file_path))
        if 'CRVAL1' not in header:
            header = fits.getheader(getFilePathRootFits(reference.file_path), ext=1)
    else:
        header = fits.getheader(getFilePathRootFits(fil[0].file_path))
    ra = str(header['CRVAL1'])
    dec = str(header['CRVAL2'])

    # Init config
    config = {
        "COPY_KEYWORDS": "EXPTIME,OBJECTDATE-OBS,AIRMASS,PI-COI,TELESCOP,INSTRUME,FILTER,PRJ_ID,PRJ_VER",
        "SUBTRACT_BACK": mar.env.marConf['Swarp']['FIRST_RUN_SUBTRACT_BACK'],
        "BACK_FILTERSIZE": mar.env.marConf['Swarp']['FIRST_RUN_BACK_FILTERSIZE'], 
        "BACK_SIZE": mar.env.marConf['Swarp']['FIRST_RUN_BACK_SIZE'],
        "PIXEL_SCALE": mar.env.marConf['Instrument']['PIXSCALE'], 
        "IMAGE_SIZE": mar.env.marConf['Swarp']['IMAGE_SIZE'],
        "CENTER_TYPE": "MANUAL", "PIXELSCALE_TYPE": "MANUAL", "WEIGHT_TYPE": "MAP_WEIGHT",
        "CENTER": f'{ra}, {dec}', "GAIN_DEFAULT": mar.env.marConf['Instrument']['MASTER_GAIN'], "CELESTIAL_TYPE": "EQUATORIAL",
        "COMBINE_TYPE": "MEDIAN"}

    config['WEIGHT_IMAGE'] = masks

    pathswarp = os.path.join(get_master_path("SWARP"), fil[0].band, fil[0].field)
    check_path(pathswarp)

    MarManager.INFO(f"Running first swarp on {fil[0].field}")

    s = mar.wrappers.Swarp(images, addconf=config, outdir=pathswarp)
    s.run()

    config = {"COPY_KEYWORDS": "OBJECTDATE-OBS,AIRMASS,PI-COI,TELESCOP,INSTRUME,FILTER,PRJ_ID,PRJ_VER",
                        "BACK_FILTERSIZE": mar.env.marConf['Swarp']['SECOND_RUN_BACK_FILTERSIZE'], 
                        "BACK_SIZE": mar.env.marConf['Swarp']['SECOND_RUN_BACK_SIZE'], 
                        "PIXEL_SCALE": mar.env.marConf['Instrument']['PIXSCALE'], 
                        "IMAGE_SIZE": mar.env.marConf['Swarp']['IMAGE_SIZE'],
                        "CENTER_TYPE": "MANUAL", "PIXELSCALE_TYPE": "MANUAL", "WEIGHT_TYPE": "MAP_WEIGHT",
                        "CENTER": f'{ra}, {dec}', "GAIN_DEFAULT": mar.env.marConf['Instrument']['MASTER_GAIN'], "RESAMPLE": "N",
                        "CELESTIAL_TYPE": "EQUATORIAL", "COMBINE_TYPE": "WEIGHTED", "SUBTRACT_BACK": "N"}

    config['WEIGHT_IMAGE'] = weights
    MarManager.INFO(f"Running second swarp on {fil[0].field}")
    s = mar.wrappers.Swarp(resamp, addconf=config, outdir=pathswarp)
    s.run()

    for item in fil:
        fpack_db(item)

    tilepath = os.path.join(get_master_path("TILES"), fil[0].field)
    check_path(tilepath)

    weightpath = os.path.join(tilepath, f'{fil[0].field}_{fil[0].band}_swpweight.fits')
    tilepath = os.path.join(tilepath, f'{fil[0].field}_{fil[0].band}_swp.fits')
    os.rename(os.path.join(pathswarp, "coadd.fits"), tilepath)
    os.rename(os.path.join(pathswarp, "coadd.weight.fits"), weightpath)

    if not mar.env.marConf['Swarp']['KEEP_INTERMEDIATE_FITS']:
        remove(os.path.join(getFilePathRootFits(pathswarp), "*.fits"))
    elif mar.env.marConf['Swarp']['FPACK_INTERMEDIATE']:
        fpack(os.path.join(getFilePathRootFits(pathswarp), "*.fits"))

    finaltile.file_path = removeRootFitsPath(tilepath)
    finaltile.weight_path = removeRootFitsPath(weightpath)

    make_thumb(tilepath, tilepath.replace("fits", "png"))
    make_thumb(weightpath, weightpath.replace("fits", "png"))

    finaltile.file_thumb = removeRootFitsPath(tilepath.replace("fits", "png"))
    finaltile.weight_thumb = removeRootFitsPath(weightpath.replace("fits", "png"))

    hdu = mar.image.marfits.fromfile(tilepath)
    hdu.updateheader(ignore_cards=["SATURATE", "GAIN", "EXPTIME"])

    x = mar.image.ComputeStats(hdu)
    x.calcallstats()
    x.updateHeader(generalOnly=True)
    hdu.writeto(tilepath, overwrite=True, compress=False)

    finaltile.modeavg = round(x.modeavg, 6)
    finaltile.medianavg = round(x.medianavg, 6)
    finaltile.noiseavg = round(x.noiseavg, 6)
    finaltile.medianrms = round(x.medianrms, 6)
    finaltile.noiserms = round(x.noiserms, 6)

    finaltile.crval1 = np.mean(crval1_mean)
    finaltile.crval2 = np.mean(crval2_mean)

    sextr = mar.reduction.SExtractorCatalog(tilepath, folder=pathswarp)
    sextr.run()

    info = mar.reduction.CatalogOperation(os.path.join(pathswarp,  "catout.param"))
    info.stars()


    psfinfo = None
    if mar.env.marConf['config']['USE_PSFEX']:
        vignetpath = os.path.join(pathswarp, "vignet.fits")
        mar.wrappers.createVignetCatalog(tilepath, output=vignetpath)
        psf = mar.wrappers.PSFex(vignetpath, folder=pathswarp)
        psf.run()
        psfinfo = psf.getPSFinfo()

    hdu = mar.image.marfits.fromfile(tilepath, mode="update")

    hdu.setCard('MAR PRO FWHMSEXT', info.FWHMSEXT, comment="FWHM arcsec estimated with Sextractor")
    hdu.setCard('MAR PRO FWHMSRMS', info.FWHMSRMS, comment="rms in FWHM with Sextractor")

    if psfinfo:
        pixscale = float(mar.env.marConf['Reduction']['PIXSCALE'])
        hdu.setCard('MAR PRO FWHMMEAN', psfinfo["FWHM_Mean"] * pixscale, comment="PSFex FWHM in arcsec")
        hdu.setCard('MAR PRO FWHMBETA', psfinfo["MoffatBeta_Mean"], comment="PSFex beta - MoffatBeta_Mean")
        hdu.setCard('MAR PRO FWHMNSTARS', psfinfo["NStars_Accepted_Total"], comment="PSFex nstars - NStars_Accepted_Total")
        hdu.setCard('MAR PRO ELLIPMEAN', psfinfo["Ellipticity_Mean"], comment="PSFex Ellipmean - Ellipticity_Mean")

    hdu.setCard('OBJECT', fil[0].field)
    hdu.setCard('NCOMBINE', len(im_names))
    
    for key, im_name in enumerate(im_names):
        hdu.setCard(f'COMB_{key}', im_name, comment="Combined on swarp")
    for key, exp in enumerate(exps):
        hdu.setCard(f'EXP_{key}', exp, comment="EXPTIME respective to COMB_N")

    hdu.flush()

    if mar.env.marConf['config']['FPACK_TILES']:
        fpack(getFilePathRootFits(finaltile.file_path), True)
        fpack(getFilePathRootFits(finaltile.weight_path), True)
        finaltile.file_path = str(finaltile.file_path) + ".fz"
        finaltile.weight_path = str(finaltile.weight_path) + ".fz"

    finaltile.save()
    for item in fil:
        finaltile.composedBy.add(item)
    finaltile.status = 1
    finaltile.flag = -1
    finaltile.save()

    sci_by_filter.finaltiles.add(finaltile)
    sci_by_filter.save()
    try: 
        field_lock.delete()
    except:
        MarManager.WARN(f"Field lock not found for {fil[0].field} {fil[0].band}")




# def make_final_catalog(item, header : astropy.io.fits.header.Header):
#     module_dir = os.path.dirname(__file__)  
#     config_path = os.path.join(module_dir, 'files/sex.seconfig')

#     sextR = mar.wrappers.readWriteCats()
#     sextR.read_config(config_path)

#     sextR.config['SATUR_LEVEL']['value'] = header['SATURATE'] 
#     sextR.config['GAIN']['value'] = header['GAIN']

#     sextR.config['MAG_ZEROPOINT']['value'] = float(ZPS[ZPS['Field'] == header['OBJECT'].replace('_', '-')]['ZP_' + header['FILTER'].lower().replace('f', 'J0')])

#     for i in header:
#         if 'FWHMSEXT' in i:
#             sextR.config['SEEING_FWHM']['value'] = header[i]
    
#     catpath = generateName("TMP", string=str(item.file_name) + ".cat", ext="")  ##Get path of output file Sextractor
    
#     path = os.path.join(get_master_path("SEXTRACTOR"), item.band, item.file_name)
#     check_path(path)
#     filepath = os.path.join(path, get_filename(catpath))
#     sextR.write_file()




## Init procClass
Reduction_Instance = ProcessReduction()

