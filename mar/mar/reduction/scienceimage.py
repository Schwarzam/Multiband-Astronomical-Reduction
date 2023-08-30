from astropy.io import fits
from mar.reduction import Scan
import os
from os.path import join, isfile, isdir
import numpy as np
from mar import env
import mar

from mar.config import MarManager
from mar.wrappers import make_thumb, delete_file

from mar.utilities import add_moon_summary_header


try:
    from pyraf import iraf
except:
    print('Could not load pyraf!')

def absoluteFilePaths(directory):
    paths = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            paths.append(os.path.abspath(os.path.join(dirpath, f)))
    
    return paths

import string
import random

class PrepareSciImages:
    """A class to prepare science images for further processing.

        Attributes:
            files: a list of science files to be processed
            outdir: output directory
            outputfiles: boolean attribute indicating whether the output files will be saved
            outname: output filename
            compress: boolean attribute indicating whether the output fits files should be compressed
            shape: the shape of the image
            gainPerAmp: boolean attribute indicating whether the gain should be applied per amplifier
            bias: bias image
            flat: flat image

        Methods:
            __init__(self, folder=None, files = None, outdir='/tmp/', compress=False): Constructor method. Initializes the class with the folder, files, output directory and compression options.
            run_overscan(self, masterBias=None, masterFlat=None, correct=True, gainPerAmp=False, subtract_bias=True, genThumb=False): Runs overscan, bias subtraction and flat correction on the science images.
            overscan(self, file, subtract_bias, genThumb): Performs overscan, bias subtraction and flat correction on a single science image.
            SuperFlat(self, files_to_fringe=None): Creates a SuperFlat image.
    """    
    def __init__(self, folder=None, files = None, outdir='/tmp/', compress=False):
        """
        Initializes a new instance of the PrepareSciImages class.

        Args:
            folder (str): The path to the folder containing the science images.
            files (list): A list of paths to the science images.
            outdir (str): The path to the output directory where the prepared images will be stored.
            compress (bool): Whether to compress the output images or not.
        """
        MarManager.INFO("Starting SCI images Class.")

        try:
            marConf = mar.AttributeDict(env.marConf)
            self.configVal = mar.AttributeDict(mar.env.marConf.Instrument)
        except:
            print('Could not load config')

        self.outdir = outdir
        self.outputfiles = False
        self.outname = ''

        if folder is not None:
            validFiles = [f for f in absoluteFilePaths(folder) if (isfile(join(folder, f)) and '.fits' in f)]
            print("Files detected: " + str(len(validFiles)))
        elif files is not None:
            validFiles = files
            self.outputfiles = True

        MarManager.INFO(f"Detected: {str(len(validFiles))} SCI files.")
        self.files = validFiles
        self.tmpfiles = []
        self.compress = compress
        self.shape = None

        self.gainPerAmp = False
        self.bias = ''
        self.flat = ''
        

    def run_overscan(self, masterBias=None, masterFlat=None, correct=True, gainPerAmp=False, subtract_bias=True, genThumb=False):
        """
        Runs overscan, bias subtraction and flat correction on the science images in parallel.

        Args:
            masterBias (str): The path to the master bias frame.
            masterFlat (str): The path to the master flat frame.
            correct (bool): Whether to correct for the bias and flat or not.
            gainPerAmp (bool): Whether to apply gain correction for each amplifier.
            subtract_bias (bool): Whether to subtract the bias from the images.
            genThumb (bool): Whether to generate a thumbnail image or not.
        """
        if (masterBias is None and correct) or (masterFlat is None and correct):
            return ('Need to fill masterBias and masterFlat with path.')

        self.gainPerAmp = gainPerAmp

        self.bias = fits.getdata(masterBias)
        self.flat = fits.getdata(masterFlat)

        try:
            ncmode = float(fits.getval(masterFlat, 'HIERARCH MAR QC NCMODE', 0))
        except:
            ncmode = float(fits.getval(masterFlat, 'HIERARCH MAR QC NCMODE', 1))

        self.flat /= ncmode

        for file in self.files:
            MarManager.submit(self.overscan, file, subtract_bias, genThumb, group="SCI")
        MarManager.wait_group_done("SCI")


    def overscan(self, file, subtract_bias, genThumb):
        """
        Performs overscan, bias subtraction and flat correction on a single science image.

        Args:
            file (str): The path to the science image.
            subtract_bias (bool): Whether to subtract the bias from the image.
            genThumb (bool): Whether to generate a thumbnail image or not.
        """

        MarManager.INFO(f"Overscan + BiasSubtraction + FlatCorrection on SCI. {file}")
        scan = Scan(file)
        scan.run()

        dataHDU = 1
        if len(scan.hdu) == 1:
            dataHDU = 0

        if self.shape is None:
            self.shape = scan.hdu[dataHDU].data.shape
        
        MarManager.INFO("Adding moon summary header")
        scan.hdu[dataHDU].header = add_moon_summary_header(scan.hdu[dataHDU].header)
       
        if self.gainPerAmp:
            amps = self.configVal['HIERARCH MAR DET OUTPUTS']
            if subtract_bias:
                scan.hdu[dataHDU].data = scan.hdu[dataHDU].data - np.asarray(self.bias, dtype=np.float32)

            for i in range(1,amps+1):
                areaGain = float(self.configVal[f'HIERARCH MAR DET OUT{i} GAIN'])

                area = mar.image.getAmpArea(i)
                scan.hdu[dataHDU].data[area[0]:area[1], area[2]:area[3]] *= areaGain

            scan.hdu.setCard('GainCorrec', 'BY AMP', 'Corrected Gain By amp')
            scan.hdu[dataHDU].data = scan.hdu[dataHDU].data / np.asarray(self.flat, dtype=np.float32)

        else:
            if subtract_bias:
                scan.hdu[dataHDU].data = scan.hdu[dataHDU].data - np.asarray(self.bias, dtype=np.float32)

            scan.hdu[dataHDU].data = scan.hdu[dataHDU].data / np.asarray(self.flat, dtype=np.float32)

        if self.outputfiles:
            scan.hdu.writetosingle(self.files[file], compress=self.compress, overwrite=True, datahdu=dataHDU)
            if genThumb:
                make_thumb(self.files[file], os.path.join(self.outdir, self.files[file].split('/')[-1].replace(".fits", "").replace(".fz", "") + ".png"))

            MarManager.INFO('Done for ' + file)   

        else:
            scan.hdu.writetosingle(os.path.join(self.outdir, "corr_" + file.split('/')[-1].strip('.fz')), compress=self.compress, overwrite=True, datahdu=dataHDU)
            MarManager.INFO('Done for ' + file) 


    def SuperFlat(self, files_to_fringe=None):
        """
        Creates a super flat field from the science images.

        Args:
            files_to_fringe (list): A list of paths to the science images.

        Returns:
            The path to the super flat field.
        """
        MarManager.INFO('Creating SuperFlat') 

        SuperflatConf = mar.AttributeDict(env.marConf.Superflat)
        InstrumentConf = mar.AttributeDict(env.marConf.Instrument)

        files = []
        fil = ''

        if files_to_fringe:
            for i in files_to_fringe:
                fil += i + '\n'

        elif self.outputfiles:
            for i in self.files:
                files.append(self.files[i])

            for i in files:
                fil += i + '\n'
            
        else:
            files = [f for f in absoluteFilePaths(self.outdir) if (isfile(join(self.outdir, f)) and '.fits' in f and f.split('/')[-1].startswith('corr_'))]

            for i in files:
                if i.split('/')[-1].startswith('corr_') and '.fits' in i:
                    fil += i + '\n'

        self.fil = fil
        self.tmpfiles = self.tmpfiles + files

        inputlst = join(self.outdir, 'input.lst')
        file = open(inputlst, 'w')
        file.write(fil)
        file.close()

        if SuperflatConf.CF_SUPERFLAT_CORRECTION == "offset":
            scale = "none"
            offsets = "mode"
        elif SuperflatConf.CF_SUPERFLAT_CORRECTION == "gain":
            scale = "mode"
            offsets = "none"
        else:
            return 'Correction not implemented.'

        if self.gainPerAmp:
            gain = 1
        else:
            gain = InstrumentConf['MASTER_GAIN']
        rdnoise = InstrumentConf['MASTER_RNOISE']

        rnd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        output = os.path.join(self.outdir, f"{rnd}SuperFlat.fits")
        self.outname = output
        self.bpmask = os.path.join(self.outdir, f"SuperFlatBPM{rnd}.fits") 

        MarManager.INFO('Starting SuperFlat IMCOMBINE') 

        
        iraf.imcombine(input="@" + inputlst,
                       output=output, headers="",
                       bpmasks=self.bpmask, rejmasks="", nrejmasks="",
                       expmasks="", sigmas="", logfile="STDOUT",
                       combine="median", reject="avsigclip", project="no",
                       outtype="real", outlimits="", offsets="none",
                       masktype="none", maskvalue=0,
                       blank=0., scale=scale,
                       zero=offsets, weight="none",
                       expname="",
                       lthresh="INDEF", hthresh="INDEF", nlow=1., nhigh=1.,
                       nkeep=1, mclip="yes", lsigma=3.,
                       hsigma=3., rdnoise=rdnoise,
                       gain=gain, snoise=0.0, sigscale=0.01, pclip=(-0.5),
                       grow=0)


        # output2 = os.path.join(self.outdir, f"minmax{rnd}SuperFlat.fits") 
        # self.bpmask2 = os.path.join(self.outdir, f"minmax_SuperFlatBPM{rnd}.fits")

        # iraf.imcombine(input="@" + inputlst,
        #                output=output2, headers="",
        #                bpmasks=self.bpmask2, rejmasks="", nrejmasks="",
        #                expmasks="", sigmas="", logfile="STDOUT",
        #                combine="median", reject="minmax", project="no",
        #                outtype="real", outlimits="", offsets="none",
        #                masktype="none", maskvalue=0,
        #                blank=0., scale=scale,
        #                zero=offsets, weight="none",
        #                expname="",
        #                lthresh="INDEF", hthresh="INDEF", nlow=3., nhigh=20.,
        #                nkeep=1, mclip="yes", lsigma=3.,
        #                hsigma=3., rdnoise=rdnoise,
        #                gain=gain, snoise=0.0, sigscale=0.01, pclip=(-0.5),
        #                grow=0)

        hdu = mar.image.marfits.fromfile(output, mode='update')

        hdu = mar.image.ComputeStats(hdu)
        hdu.calcallstats()
        hdu.updateHeader()
        
        hdu = hdu.hdu
        hdu.flush()

        self.superflat = hdu
        MarManager.INFO('Finished SuperFlat IMCOMBINE')



def SuperFlatMask(image = None, outdir="/tmp/"):
    """
    Generates a mask for a science image.

    Args:
        image (str): The path to the science image.
        outdir (str): The path to the output directory where the mask will be stored.
    """
    mar.wrappers.FilterSky(image, outdir, BACK_FILTERSIZE = 1, BACK_SIZE=32, 
        DETECT_THRESH=1000, DETECT_MINAREA=10, 
        ANALYSIS_THRESH=100, CHECKIMAGE_TYPE="BACKGROUND")


'''
sci = mar.reduction.PrepareSciImages(testbloc, outdir = '/home/gustavo/Documents/CorrSci/')

sci.run_overscan(masterBias='/home/gustavo/Documents/t.fits.fz', masterFlat='/home/gustavo/Documents/MasterFlat.fits')
sci.SuperFlat()

sci.hdu.writetosingle(path)

'''


'''
flat = (flat-bias) * gain
obj = (obj-bias) * gain

obj / flat 
'''
