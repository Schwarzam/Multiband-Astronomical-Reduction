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

try:
	configVal = mar.AttributeDict(mar.env.marConf.Instrument)
except:
	print('Could not get instrument config.')

def absoluteFilePaths(directory):
	paths = []
	for dirpath,_,filenames in os.walk(directory):
		for f in filenames:
			paths.append(os.path.abspath(os.path.join(dirpath, f)))
	
	return paths


class MasterBias:
	"""
	Class to perform MasterBias operations.

	Attributes:
		outdir (str): directory where all results will be saved
		perAmp (bool): run iraf per amplifier
		amps (int): number of amplifiers
		ampSize (tuple): size of the amplifier region
		orders (numpy.array): amplifier orders
		indices (numpy.array): amplifier indices
		files (list): list with all file paths
		shape (tuple): shape of the image
		tmpfiles (list): list with intermediate file paths

	Methods:
		__init__(self, folder=None, files=None, outdir='/tmp/', perAmp=False):
			Initializes the MasterBias class.

		run_overscan(self, genThumb=False):
			Run overscan on files loaded to MasterBias Class.

		overscan(self, file, genThumb):
			Run overscan routine.

		run_imcombine(self, delete_after=True):
			Run iraf IMCOMBINE on files loaded on class.
			These files must be overscanned before running IRAF.

		getBPM(self):
			Generates Bad Pixel Mask (hotmask) for incombined result.

		del_procfiles(self):
			Delete intermediate files.
	"""
	def __init__(self, folder=None, files=None, outdir='/tmp/', perAmp=False):
		"""Class to perform MasterBias operations. 

		Args:
			folder (str, optional): folder path to get all items in folder, usually not ideal. Defaults to None.
			files (list, optional): list with all file paths, ideal way to input files. Defaults to None.
			outdir (str, optional): directory where all results will be saved. Defaults to '/tmp/'.
			perAmp (bool, optional): run iraf per amplifier. Defaults to False.
		"""		
		MarManager.INFO("Starting MasterBias Class")
		self.outdir = outdir
		self.perAmp = perAmp

		ampSize = mar.utilities.conversion.str2coordinate(configVal['HIERARCH MAR DET OUT1 IMSC'])
		self.amps = configVal['HIERARCH MAR DET OUTPUTS']

		self.ampSize = (ampSize[1] - ampSize[0], ampSize[3] - ampSize[2])
		self.orders = np.array([[1, 2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15, 16]])
		self.indices = np.indices(self.orders.shape)

		if folder is not None:
			validFiles = [f for f in absoluteFilePaths(folder) if (isfile(join(folder, f)) and '.fits' in f)]

		elif files is not None:
			validFiles = files

		MarManager.INFO(f'Detected {str(len(validFiles))} BIAS files.')
		if len(validFiles) < 30:
			MarManager.WARN(f'Low BIAS files count: {str(len(validFiles))}.')

		self.files = validFiles
		self.shape = None

		self.tmpfiles = []

	def run_overscan(self, genThumb=False):
		"""Run overscan on files loaded to MasterBias Class

		Args:
			genThumb (bool, optional): Generate Image from done overscan file. Defaults to False.
		"""		
		for file in self.files:
			MarManager.submit(self.overscan, file, genThumb, group="BIAS")
		MarManager.wait_group_done("BIAS")


	def overscan(self, file, genThumb):
		"""Run overscan routine

		Args:
			file (str): filename
			genThumb (bool): generate image from result
		"""		
		ampSize = self.ampSize
		indices = self.indices
		orders = self.orders

		MarManager.INFO(f"Running ovsc on BIAS {get_filename(file)}")
		scan = Scan(file)
		scan.run()

		if self.shape is None:
			self.shape = scan.hdu[1].data.shape

		data = scan.hdu[1].data.copy()

		if genThumb:
			scan.hdu[1].data = data
			name = os.path.join(self.outdir, "OVSC" + "_" + file.split('/')[-1].strip('.fz'))
			outn = name.replace(".fits", "").replace(".fz", "") + ".png"
			scan.hdu.writetosingle(name, compress=False, overwrite=True)
			make_thumb(name, outn)


		if self.perAmp:
			for i in range(1, self.amps+1):
				if not os.path.exists(os.path.join(self.outdir, f'AMP{i}')):
					os.mkdir(os.path.join(self.outdir, f'AMP{i}'))

				y = indices[0][(orders == i)][0]
				x = indices[1][(orders == i)][0]

				image_section = [y * ampSize[0], (y + 1) * ampSize[0], x * ampSize[1], (x + 1) * ampSize[1]]
				scan.hdu[1].data = data[image_section[0]: image_section[1], image_section[2]: image_section[3]]
				scan.hdu.writetosingle(os.path.join(self.outdir, f'AMP{i}', "AMP" + str(i) + "_" + file.split('/')[-1].strip('.fz')), compress=False, overwrite=True)
		
		elif not genThumb:
			name = os.path.join(self.outdir, "OVSC" + "_" + file.split('/')[-1].strip('.fz'))
			outn = name.replace(".fits", "").replace(".fz", "") + ".png"
			scan.hdu.writetosingle(name, compress=False, overwrite=True)

		del scan
		del data

		MarManager.INFO(f"Done {get_filename(file)}")

	def run_imcombine(self, delete_after=True):
		"""Run iraf IMCOMBINE on files loaded on class
		These files must be overscanned before running IRAF

		Args:
			delete_after (bool, optional): Delete intermediate files after done. Defaults to True.
		"""		
		rdnoise = configVal['MASTER_RNOISE']
		gain = configVal['MASTER_GAIN']

		MarManager.INFO(f"Starting Iraf IMCOMBINE on BIAS files starting with AMP(prefix) on outdir.")
		files = [f for f in absoluteFilePaths(self.outdir) if (isfile(join(self.outdir, f)) and '.fits' in f and f.split('/')[-1].startswith('AMP'))]

		self.tmpfiles = self.tmpfiles + files

		if self.perAmp:
			for amp in range(1, self.amps + 1):
				MarManager.INFO(f"IMCOMBINE on amplifier {amp} out of {self.amps}.")
				files = [f for f in absoluteFilePaths(os.path.join(self.outdir, f'AMP{amp}')) if (isfile(join(self.outdir, f'AMP{amp}', f)) and '.fits' in f and f.split('/')[-1].startswith('AMP'))]
				fil = ''
				
				for i in files:
					if i.split('/')[-1].startswith('AMP' + str(amp) + '_') and '.fits' in i:
						fil += i + '\n'

				inputlst = join(self.outdir, f'input{amp}.lst')
				file = open(inputlst, 'w')
				file.write(fil)
				file.close()

				iraf.flpr()
				iraf.flpr()
				output = os.path.join(self.outdir, "MasterBias_" + str(amp) + '.fits')
					
				rdnoise = configVal['MASTER_RNOISE']
				gain = configVal['MASTER_GAIN']

				if self.perAmp:
					gain = float(configVal[f'HIERARCH MAR DET OUT{amp} GAIN'])

				self.tmpfiles = self.tmpfiles + [output]


				iraf.imcombine(input='@' + inputlst,
									   output=output, headers="",
									   bpmasks="", rejmasks="", nrejmasks="",
									   expmasks="", sigmas="",
									   combine="median", reject="ccdclip", project="no",
									   outlimits="", offsets="none",outtype="real", 
									   masktype="none", maskvalue=0, blank=0.,
									   scale="none",
									   zero="mode", weight="none",
									   expname="EXPTIME",
									   lthresh="INDEF", hthresh="INDEF", nlow=1., nhigh=1.,
									   nkeep=1, mclip="yes", lsigma=3.,
									   hsigma=3., rdnoise=rdnoise,
									   gain=gain, snoise=0.0, sigscale=0.01,
									   pclip=(-0.5), grow=0)

			ampSize = self.ampSize
			indices = self.indices
			orders = self.orders
			newdata = np.zeros(self.shape)
			MarManager.INFO(f"Joining images again to form final MasterBias")

			for i in range(1, self.amps+1):
				fitsfile = fits.open(os.path.join(self.outdir, "MasterBias_" + str(i)) + '.fits')
				ndata = fitsfile[0].data

				y = indices[0][(orders == i)][0]
				x = indices[1][(orders == i)][0]

				image_section = [y * ampSize[0], (y + 1) * ampSize[0], x * ampSize[1], (x + 1) * ampSize[1]]
				newdata[image_section[0]: image_section[1], image_section[2]: image_section[3]] = ndata
				
			MarManager.INFO(f"MasterBias Done")
			self.hdu = mar.image.marfits([fits.PrimaryHDU(header=fitsfile[0].header, data=newdata)])

		else:
			MarManager.INFO(f"IMCOMBINE on BIAS BLOCK")
			
			fil = ''
			for file in self.files:
				name = os.path.join(self.outdir, "OVSC" + "_" + file.split('/')[-1].strip('.fz'))
				fil += name + '\n'

			inputlst = join(self.outdir, f'inputBIAS.lst')
			file = open(inputlst, 'w')
			file.write(fil)
			file.close()

			iraf.flpr()
			iraf.flpr()
			output = os.path.join(self.outdir, "MasterBias_total.fits")
				
			rdnoise = configVal['MASTER_RNOISE']
			gain = configVal['MASTER_GAIN']

			self.tmpfiles = self.tmpfiles + [output]


			iraf.imcombine(input='@' + inputlst,
								   output=output, headers="", statsec = configVal['HIERARCH MAR DET OUT1 IMSC'],
								   bpmasks="", rejmasks="", nrejmasks="",
								   expmasks="", sigmas="",
								   combine="median", reject="ccdclip", project="no",
								   outlimits="", offsets="none",outtype="real", 
								   masktype="none", maskvalue=0, blank=0.,
								   scale="none",
								   zero="mode", weight="none",
								   expname="EXPTIME",
								   lthresh="INDEF", hthresh="INDEF", nlow=1., nhigh=1.,
								   nkeep=1, mclip="yes", lsigma=3.,
								   hsigma=3., rdnoise=rdnoise,
								   gain=gain, snoise=0.0, sigscale=0.01,
								   pclip=(-0.5), grow=0)

			

			self.hdu = mar.image.marfits.fromfile(output)
			MarManager.INFO(f"Done IMCOMBINE.")
			

	def getBPM(self):
		"""Generates Bad Pixel Mask (hotmask) for incombined result 
		"""		
		mask = mar.image.computeHotMask(self.hdu[0].data)
		MarManager.INFO(f"Computed hotmask")
		self.bpmask = mar.image.marfits([fits.PrimaryHDU(data=mask)])

	def del_procfiles(self):
		"""Delete intermediate files
		"""		
		files = [f for f in absoluteFilePaths(self.outdir) if (isfile(join(self.outdir, f)) and '.fits' in f and f.split('/')[-1].startswith('AMP'))]

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
import mar

mbias = mar.reduction.MasterBias(folder = '/home/gustavo/Documents/t80testblock/BIAS')
mbias.run_overscan()

mbias.run_imcombine()
mbias.shape = (9232, 9216)
mbias.getBPM()

mbias.bpmask.writeto('/home/gustavo/Documents/mask.fits')
mbias.hdu.writeto('/home/gustavo/Documents/MBias.fits')
'''