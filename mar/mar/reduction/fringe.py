import mar
import numpy as np
from mar.utilities import BlockAverage, percfilter
from astropy.io import fits

marConf = mar.AttributeDict(mar.env.marConf.Fringe)

from mar.config import MarManager

class FringeSubtract:
	"""
	Class that performs the subtraction of fringes (interference patterns) in astronomical images.

	Methods:
	--------
	__init__(self, superFlat):
		Constructor method that reads the super-flat file, computes statistics, updates the header and sets the
		HDU and number of output detectors.
	subtractMode(self, individualAmps=False):
		Method that creates the fringe subtraction, subtracting the mode of the fringe from the image.
	ComputeContrast(self, hdu=None, headerHDU=0, dataHDU=0):
		Method that computes the fringe contrast using Block Average and percentile filtering.
	ComputeBackgroundfactor(self, im, imdataHDU=1, outim='/tmp/im.fits'):
		Method that subtracts the fringe contrast from the image.
	"""
	def __init__(self, superFlat):
		"""
		Constructor method that reads the super-flat file, computes statistics, updates the header and sets the
		HDU and number of output detectors.

		Parameters:
		-----------
		superFlat : str
			The filename of the super-flat file.
		"""
		MarManager.INFO("Starting Fringe Class")
		sf = mar.image.marfits.fromfile(superFlat)
		sf = mar.image.ComputeStats(sf)
		sf.calcallstats()
		sf.updateHeader()
		
		self.hdu = sf.hdu
		self.amps = self.hdu[0].header["MAR DET OUTPUTS"]
		
	def subtractMode(self, individualAmps=False):
		"""
		Method that creates the fringe subtraction, subtracting the mode of the fringe from the image.

		Parameters:
		-----------
		individualAmps : bool, optional
			If True, subtract the mode of the fringe for each amplifier separately. If False (default),
			subtract the mean mode of the fringe for all amplifiers.

		Returns:
		--------
		None
		"""
		MarManager.INFO("Creating fringe subtraction")
		datatoremove = []
		for amp in range(1, self.amps + 1):
			datatoremove.append(self.hdu[0].header[f"MAR QC OUT{amp} NCMODE"])
		
		if not individualAmps:
			m = np.mean(datatoremove)
			datatoremove = len(datatoremove) * [m]
		
		for amp in range(1, self.amps + 1):
			imsc = self.hdu[0].header[f"MAR PRO OUT{amp} IMSC"]
			sect = mar.utilities.str2coordinate(imsc)
			self.hdu[0].data[sect[0]:sect[1], sect[2]:sect[3]] -= datatoremove[amp - 1]


	def ComputeBackgroundfactor(self, im, imdataHDU=1, outim='/tmp/im.fits'):
		"""
		Method that subtracts the fringe contrast from the image.

		Parameters:
		-----------
		im : str
			The filename of the image to be corrected.
		imdataHDU : int, optional
			The HDU containing the data. The default is 1.
		outim : str, optional
			The filename of the corrected image. The default is '/tmp/im.fits'.

		Returns:
		--------
		None
		"""
		MarManager.INFO("Subtracting fringe contrast.")
		im = fits.open(im)
		imdata = im[imdataHDU].data

		fringescaledback = self.hdu[0].header['MAR QC NCMODE']
		_modei, _mediani, _meani, _stdi, _q1_i, _q2_i = mar.utilities.arrStats(imdata)

		frigfac = _modei / fringescaledback

		fringdata = self.hdu[0].data * frigfac
		imdata -= fringdata

		im[imdataHDU].data = imdata
		im = mar.image.marfits(hdus=im)

		self.hdu = im


'''
frin = FringeSubtract(path + 'SuperFlat.fits')
frin.subtractMode()
frin.ComputeBackgroundfactor('Documents/t80testblock/scienceTestNormalMean.fits.fz', outim='Documents/t80testblock/removedfrin.fits')
'''