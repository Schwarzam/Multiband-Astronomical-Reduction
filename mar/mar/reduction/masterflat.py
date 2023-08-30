import mar

try:
	from pyraf import iraf
except:
	pass

import os
from os.path import join, isfile, isdir

from mar.reduction import Scan
from astropy.io import fits
import numpy as np

from mar.config import MarManager

from mar.utilities import get_filename
from mar.wrappers import make_thumb, delete_file


def absoluteFilePaths(directory):
	paths = []
	for dirpath,_,filenames in os.walk(directory):
		for f in filenames:
			paths.append(os.path.abspath(os.path.join(dirpath, f)))
	
	return paths

class MasterFlat:
	"""Class to perform MasterFlat operations.

	Attributes:
		outdir (str): directory where all results will be saved.
		files (list): list with all file paths.
		shape (tuple): tuple with the dimensions of each element of files list.
		tmpfiles (list): list with all temporary files.
		gainPerAmp (bool): calculate GAIN per amp and run IRAF per amplifier (DEPRECATED).
		outfiles (list): list with all output file paths.
		masterbias (str): path to masterbias file.
		hdu: instance of mar.image.marfits.
		bpmask: instance of mar.image.marfits.

	Args:
		folder (str, optional): folder path to get all items in folder, usually not ideal. Defaults to None.
		files (list, optional): list with all file paths, ideal way to input files. Defaults to None.
		outdir (str, optional): directory where all results will be saved. Defaults to '/tmp/'.

	"""
	def __init__(self, folder=None, files=None, outdir='/tmp/'):
		"""Class to perform MasterFlat operations. 

		Args:
			folder (str, optional): folder path to get all items in folder, usually not ideal. Defaults to None.
			files (list, optional): list with all file paths, ideal way to input files. Defaults to None.
			outdir (str, optional): directory where all results will be saved. Defaults to '/tmp/'.
		"""	
		MarManager.INFO("Started Flats Class")

		try:
			self.configVal = mar.AttributeDict(mar.env.marConf.Instrument)
		except:
			print('Could not get Instrument conf.')


		self.outdir = outdir

		if folder is not None:
			validFiles = [f for f in absoluteFilePaths(folder) if (isfile(join(folder, f)) and '.fits' in f)]

		elif files is not None:
			validFiles = files

		MarManager.INFO(f'Detected {str(len(validFiles))} FLATs files.')
		if len(validFiles) < 10:
			MarManager.WARN(f'Low FLATS files count: {str(len(validFiles))}.')

		self.files = validFiles
		self.shape = None

		self.tmpfiles = []
		self.gainPerAmp = False
		self.outfiles = []
		self.masterbias = ''


	def run_overscan(self, masterBias=None, subtract_bias=True, gainPerAmp=False, genThumb=False):
		"""Run overscan on threads of files loaded to masterFlat class.

		Args:
			masterBias (str, optional): masterBias path to perform subtraction of file. Defaults to None.
			subtract_bias (bool, optional): perform BIAS subtraction, if true must give masterBias path. Defaults to True.
			gainPerAmp (bool, optional): calculate GAIN per amp and run IRAF per amplifier (DEPRECATED). Defaults to False.
			genThumb (bool, optional): Generate image of intermediates. Defaults to False.
		"""		
		self.gainPerAmp = gainPerAmp

		if masterBias is None and subtract_bias:
			MarManager.CRITICAL(f"Need to fill masterBias with path.")

		self.masterbias = fits.getdata(masterBias)

		for file in self.files:
			MarManager.submit(self.overscan, file, masterBias, subtract_bias, gainPerAmp, genThumb, group="FLAT")
		MarManager.wait_group_done("FLAT")


	def overscan(self, file, masterBias, subtract_bias, gainPerAmp, genThumb):
		"""Run overscan on single file.

		Args:
			file (_type_): flat file to perform overscan
			masterBias (_type_): masterBias path to perform subtraction of file. Defaults to None.
			subtract_bias (_type_): perform BIAS subtraction, if true must give masterBias path.
			gainPerAmp (_type_): calculate GAIN per amp and run IRAF per amplifier (DEPRECATED).
			genThumb (_type_): Generate image of intermediates. Defaults to False.
		"""		
		MarManager.INFO(f"Running ovsc on FLAT {get_filename(file)}")
		scan = Scan(file)
		scan.run()

		if self.shape is None:
			self.shape = scan.hdu[1].data.shape

		if subtract_bias:
			scan.hdu[1].data = scan.hdu[1].data - self.masterbias

		if gainPerAmp:
			amps = self.configVal['HIERARCH MAR DET OUTPUTS']
			for i in range(1,amps+1):
				areaGain = float(self.configVal[f'HIERARCH MAR DET OUT{i} GAIN'])

				area = mar.image.getAmpArea(i)
				scan.hdu[1].data[area[0]:area[1], area[2]:area[3]] *= areaGain

			scan.hdu.setCard('GainCorrec', 'BY AMP', 'Corrected Gain By amp')

		name = os.path.join(self.outdir, "OVSC__" + file.split('/')[-1].strip('.fz'))
		scan.hdu.writetosingle(name, compress=False, overwrite=True)
		if genThumb:
			outn = name.replace(".fits", "").replace(".fz", "") + ".png"
			make_thumb(name, outn)

		self.outfiles.append(os.path.join(self.outdir, "OVSC__" + file.split('/')[-1].strip('.fz')))
		MarManager.INFO(f"Done {get_filename(file)}")

	def run_imcombine(self, delete_after=True, name=None):
		"""Run iraf Imcombine on files loaded on class. They must be overscanned before. 

		Args:
			delete_after (bool, optional): Delete tmp files after. Defaults to True.
			name (str, optional): name to masterFlat file. Defaults to None. If None, name will be MasterFlat.fits
		"""		
		MarManager.INFO("Starting FLATS IMCOMBINE.")
		if self.gainPerAmp:
			gain = 1
		else:
			gain = self.configVal['MASTER_GAIN']

		rdnoise = self.configVal['MASTER_RNOISE']


		files = [f for f in absoluteFilePaths(self.outdir) if (isfile(join(self.outdir, f)) and '.fits' in f and f.split('/')[-1].startswith('OVSC__'))]
		self.tmpfiles = self.tmpfiles + files


		fil = ''
		if self.outfiles != []:
			for i in self.outfiles:
				fil += i + '\n'
		else:
			for i in files:
				if i.split('/')[-1].startswith('OVSC__') and '.fits' in i:
					fil += i + '\n'

		inputlst = join(self.outdir, 'input.lst')
		file = open(inputlst, 'w')
		file.write(fil)
		file.close()

		iraf.flpr()
		iraf.flpr()

		if name is None:
			name = "MasterFlat.fits"

		output = os.path.join(self.outdir, name)	
		self.tmpfiles = self.tmpfiles + [output]
		self.masterfile = output


		iraf.imcombine(input='@' + inputlst,
					   output=output, headers="", statsec = self.configVal['HIERARCH MAR DET OUT1 IMSC'],
					   bpmasks="", rejmasks="", nrejmasks="",
					   expmasks="", sigmas="",
					   combine="median", reject="avsigclip", project="no",
					   outlimits="", offsets="none",outtype="real", 
					   masktype="none", maskvalue=0, blank=0.,
					   scale="mode",
					   zero="none", weight="none",
					   expname="EXPTIME",
					   lthresh="INDEF", hthresh="INDEF", nlow=1., nhigh=1.,
					   nkeep=1, mclip="yes", lsigma=3.,
					   hsigma=3., rdnoise=rdnoise,
					   gain=gain, snoise=0.0, sigscale=0.01,
					   pclip=(-0.5), grow=0)

		self.hdu = mar.image.marfits.fromfile(output, mode="update")
		MarManager.INFO("IMCOMBINE Done.")
		self.hdu.updateheader()	

		MarManager.INFO("Updating MasterFlat Header.")

		sf  = mar.image.ComputeStats(self.hdu)
		sf.calcallstats()
		sf.updateHeader()


		if self.gainPerAmp:
			self.hdu.setCard("GainCorrec", "BY_AMP", "Corrected GAIN by amp")
		else:
			self.hdu.setCard("GainCorrec", "MasterGain")

		self.hdu.flush()


	def getBPM(self, filename=None):
		"""Compute cold mask to incombined masterflat

		Args:
			filename (str, optional): masterflat file name. Defaults to None.
		"""		
		MarManager.INFO("Computing coldmask.")
		if filename:
			mask = mar.image.computeColdMask(filename, outfolder=self.outdir)
		else:
			mask = mar.image.computeColdMask(self.masterfile, outfolder=self.outdir)

		self.bpmask = mar.image.marfits([fits.PrimaryHDU(data=mask)])

	def del_procfiles(self):
		
		files = [f for f in absoluteFilePaths(self.outdir) if (isfile(join(self.outdir, f)) and '.fits' in f and f.split('/')[-1].startswith('OVSC__'))]

		for i in files:
			try:
				os.remove(i)
			except:
				pass

		for i in self.tmpfiles:
			try:
				os.remove(i)
			except:
				pass


'''
mflat = mar.reduction.MasterFlat(folder = '/home/gustavo/Documents/t80testblock/FLAT')
mflat.run_overscan(masterBias='/home/gustavo/Documents/t.fits.fz')
mflat.run_imcombine()
mflat.hdu.writeto(path)

mflat.getBPM()
mflat.del_procfiles()
mflat.bpmask.writeto(path)

'''