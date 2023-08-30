import mar
import os

from mar.wrappers.wrappersoperation import *
from mar.wrappers.terminal import runCommand

from mar.config import MarManager

marConf = mar.AttributeDict(mar.env.marConf.Sextractor)

class SExtr(readWriteCats):
	"""
	Class for running sextractor on an image.

	Args:
	- image (str): Path to the image file.
	- addconf (dict): Dictionary containing additional configurations for sextractor. Default is None.
	- defaultconf (dict): Dictionary containing default configurations for sextractor. Default is None.
	- read_addconf (str): Path to an existing config file to be loaded as additional configurations. Default is None.
	- read_defaultconf (str): Path to an existing config file to be loaded as default configurations. Default is None.
	- folder (str): Folder where the output files will be saved. Default is '/tmp/'.
	- command (str): Path to the sextractor executable file. Default is 'sex'.
	- catname (str): Name of the output catalog file. Default is 'catout.param'.

	Attributes:
	- config (dict): Dictionary containing the sextractor configuration.
	- params (list): List containing the names of the parameters to be extracted by sextractor.
	
	Methods:
	- run(): Runs sextractor with the current configuration and the specified image file.

	"""
	def __init__(self, image=None, addconf=None, defaultconf=None, read_addconf=None, read_defaultconf=None, folder='/tmp/', command='sex', catname = "catout.param"):
		readWriteCats.__init__(self)

		self.command = command
		self.image = image
		self.path = folder

		try:
			self.configVal = mar.AttributeDict(mar.env.marConf.Instrument)
		except:
			print('Could not get instrument config.')
		
		self.config = {'BACK_FILTERSIZE': {'value': 3, 'comment': ''},
						 'BACK_SIZE': {'value': 128, 'comment': ''},
						 'BACK_TYPE': {'value': 'AUTO', 'comment': ''},
						 'BACK_VALUE': {'value': '0.0,0.0', 'comment': ''},
						 'THRESH_TYPE': {'value': 'RELATIVE', 'comment': ''},
						 'ANALYSIS_THRESH': {'value': 1.5, 'comment': ''},
						 'DETECT_THRESH': {'value': 1.5, 'comment': ''},
						 'DETECT_MINAREA': {'value': 5, 'comment': ''},
						 'FILTER_THRESH': {'value': '', 'comment': ''},
						 'FILTER': {'value': 'Y', 'comment': ''},
						 'FILTER_NAME': {'value': os.path.join(mar.__path__[0], 'config/sextractor/default.conv'), 'comment': ''},
						 'CLEAN': {'value': 'Y', 'comment': ''},
						 'CLEAN_PARAM': {'value': 1.0, 'comment': ''},
						 'DEBLEND_NTHRESH': {'value': 32, 'comment': ''},
						 'DEBLEND_MINCONT': {'value': 0.005, 'comment': ''},
						 'MASK_TYPE': {'value': 'CORRECT', 'comment': ''},
						 'WEIGHT_TYPE': {'value': 'BACKGROUND', 'comment': ''},
						 'WEIGHT_IMAGE': {'value': os.path.join('weight.fits'), 'comment': ''},
						 'WEIGHT_THRESH': {'value': '', 'comment': ''},
						 'WEIGHT_GAIN': {'value': 'Y', 'comment': ''},
						 'GAIN': {'value': self.configVal['MASTER_GAIN'], 'comment': ''},
						 'GAIN_KEY': {'value': 'GAIN', 'comment': ''},
						 'FLAG_IMAGE': {'value': 'flag.fits', 'comment': ''},
						 'FLAG_TYPE': {'value': 'OR', 'comment': ''},
						 'BACKPHOTO_TYPE': {'value': 'LOCAL', 'comment': ''},
						 'BACKPHOTO_THICK': {'value': 24, 'comment': ''},
						 'BACK_FILTTHRESH': {'value': 0.0, 'comment': ''},
						 'PHOT_AUTOPARAMS': {'value': (2.5, 3.5), 'comment': ''},
						 'PHOT_AUTOAPERS': {'value': (0.0, 0.0), 'comment': ''},
						 'PHOT_PETROPARAMS': {'value': (2.0, 3.5), 'comment': ''},
						 'PHOT_APERTURES': {'value': (2, 28, 160), 'comment': ''},
						 'PHOT_FLUXFRAC': {'value': 0.5, 'comment': ''},
						 'SATUR_LEVEL': {'value': self.configVal['SATURATE'], 'comment': ''},
						 'SATUR_KEY': {'value': 'SATURATE', 'comment': ''},
						 'STARNNW_NAME': {'value': os.path.join(mar.__path__[0], 'config/sextractor/default.nnw'), 'comment': ''},
						 'SEEING_FWHM': {'value': 1.1, 'comment': ''},
						 'CATALOG_NAME': {'value': os.path.join(folder, catname), 'comment': ''},
						 'PARAMETERS_NAME': {'value': os.path.join(folder, 'params.sex'), 'comment': ''},
						 'CHECKIMAGE_TYPE': {'value': ('SEGMENTATION', 'APERTURES', 'OBJECTS'),
						  'comment': ''},
						 'CHECKIMAGE_NAME': {'value': ('tmp_SEGM.fits',
						   'tmp_APER.fits',
						   'tmp_OBJ.fits'),
						  'comment': ''},
						 'INTERP_TYPE': {'value': 'NONE', 'comment': ''},
						 'INTERP_MAXYLAG': {'value': 4, 'comment': ''},
						 'INTERP_MAXXLAG': {'value': 4, 'comment': ''},
						 'DETECT_TYPE': {'value': 'CCD', 'comment': ''},
						 'MEMORY_BUFSIZE': {'value': 11000, 'comment': ''},
						 'MEMORY_PIXSTACK': {'value': 3000000, 'comment': ''},
						 'MEMORY_OBJSTACK': {'value': 10000, 'comment': ''},
						 'PIXEL_SCALE': {'value': 0.55, 'comment': ''},
						 'MAG_GAMMA': {'value': 4.0, 'comment': ''},
						 'MAG_ZEROPOINT': {'value': 25.0, 'comment': ''},
						 'CATALOG_TYPE': {'value': 'FITS_LDAC', 'comment': ''},
						 'VERBOSE_TYPE': {'value': 'NORMAL', 'comment': ''},
						 'WRITE_XML': {'value': 'Y', 'comment': ''},
						 'XML_NAME': {'value': '/tmp/sexout.xml', 'comment': ''},
						 'NTHREADS': {'value': marConf.NTHREADS, 'comment': ''}
			}
		
		
		self.params = [
						'NUMBER',
						'X_IMAGE',
						'Y_IMAGE',
						'MAG_AUTO',
						'MAGERR_AUTO',
						'FLUX_ISO',
						'FLUXERR_ISO',
						'MAG_ISO',
						'MAGERR_ISO',
						'FLUX_ISOCOR',
						'FLUXERR_ISOCOR',
						'MAG_ISOCOR',
						'MAGERR_ISOCOR',
						'FLUX_APER(3)',
						'FLUXERR_APER(3)',
						'MAG_APER(3)',
						'MAGERR_APER(3)',
						'FLUX_RADIUS',
						'FLUX_AUTO',
						'FLUXERR_AUTO',
						'BACKGROUND',
						'FLUX_MAX',
						'FWHM_IMAGE',
						'FWHM_WORLD'
			]
		
		if addconf:
			if isinstance(addconf, dict):
				for i in addconf:
					self.config[i]['value'] = addconf[i]
		
		if read_addconf:
			self.read_config(read_addconf, overwrite_config=False)
		
		if read_defaultconf:
			self.read_config(read_defaultconf, overwrite_config=True)
			
		if defaultconf:
			self.config = defaultconf
			self.convert()
 
	def run(self):
		"""Runs sextractor with the current configuration and the specified image file.
		"""        
		if self.image is None:
			return ('Image not found')
		
		self.confile = os.path.join(self.path, 'config.sex')
		self.write_file(self.confile)
		self.write_params()
		
		MarManager.INFO('SExtr - Running sextractor')
		command = self.command + ' ' + self.image + ' -c ' + self.confile

		code = runCommand(command, timeout = marConf.TIMEOUT)
		
		MarManager.INFO('sextractor ran with code ' + str(code))



def FilterSky(image, outfolder, BACK_FILTERSIZE = 1, BACK_SIZE=21, DETECT_THRESH=1000, DETECT_MINAREA=10, 
			 ANALYSIS_THRESH=100, CHECKIMAGE_TYPE=None, CHECKIMAGE_NAME="im.fits", WEIGHT_IMAGE="weight.fits",
			 CATALOG_NAME="out.cat"):
	"""
	Runs sextractor on an image to create a catalog, and save it to the specified output folder.
	
	Args:
	- image (str): Path to the image file.
	- outfolder (str): Folder where the output files will be saved.
	- BACK_FILTERSIZE (int): Background filter size for sextractor. Default is 1.
	- BACK_SIZE (int): Background mesh size for sextractor. Default is 21.
	- DETECT_THRESH (float): Detection threshold for sextractor. Default is 1000.
	- DETECT_MINAREA (int): Minimum number of connected pixels for detection by sextractor. Default is 10.
	- ANALYSIS_THRESH (float): Threshold for analysis by sextractor. Default is 100.
	- CHECKIMAGE_TYPE (str or None): Type of the check image to be created by sextractor. If None, no check image will be created. Default is None.
	- CHECKIMAGE_NAME (str): Name of the check image file. Default is 'im.fits'.
	- WEIGHT_IMAGE (str): Name of the weight image file. Default is 'weight.fits'.
	- CATALOG_NAME (str): Name of the catalog file. Default is 'out.cat'.

	"""
	WEIGHT_TYPE = "BACKGROUND"
	
	if CHECKIMAGE_TYPE is None:
		CHECKIMAGE_TYPE = "NONE"
	
	conf = {"BACK_FILTERSIZE": BACK_FILTERSIZE,
		"BACK_SIZE": BACK_SIZE,
		"DETECT_THRESH": DETECT_THRESH,
		"DETECT_MINAREA": DETECT_MINAREA,
		"ANALYSIS_THRESH": ANALYSIS_THRESH,
		"FILTER": "N",
		"CATALOG_NAME": os.path.join(outfolder, CATALOG_NAME),
		"CHECKIMAGE_TYPE": CHECKIMAGE_TYPE,
		"CHECKIMAGE_NAME": os.path.join(outfolder, CHECKIMAGE_NAME),
		"WEIGHT_TYPE": WEIGHT_TYPE,
		"WEIGHT_IMAGE": os.path.join(outfolder, WEIGHT_IMAGE)}
	
	inst = SExtr(image=image , folder=outfolder, addconf=conf)
	inst.run()