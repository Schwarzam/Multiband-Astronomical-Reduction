from astropy.io import fits
from astropy.io.fits import HDUList, CompImageHDU, getdata
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore", message="Keyword name")

import mar
from mar import env, AttributeDict

from mar.config import MarManager

class MaskArray(np.ndarray):
	"""
	A class to handle masks within an array, extending numpy.ndarray.

	...

	Methods
	-------
	add_mask(mask : np.ndarray, value : int)
		Add a mask with a certain value to the array.
	get_mask(values : List[int], binary : bool = False) -> np.ndarray
		Get a mask from the array corresponding to certain values.
	"""

	def __new__(cls, input_array):
		"""
		Create a new instance of the class. This method is necessary because numpy.ndarray is a non-Python type.

		Parameters
		----------
		input_array : array-like
			The input array to be converted into a MaskArray.

		Returns
		-------
		obj : MaskArray
			The input array as a MaskArray object.
		"""
		obj = np.asarray(input_array).view(cls)
		return obj

	def add_mask(self, mask, value):
		"""
		Add a mask with a certain value to the array.

		Parameters
		----------
		mask : np.ndarray
			The mask to be added. Should be an array of 0s and 1s of the same shape as the MaskArray.
		value : int
			The value to assign to the mask. Should be a power of 2 to allow bitwise operations.
		"""
		self += mask * value

	def get_mask(self, values, binary=False, inverted=False, dtype='uint8'):
		"""
		Get a mask from the array corresponding to certain values.

		Parameters
		----------
		values : List[int]
			A list of the mask values to include in the output mask.
		binary : bool, optional
			If True, return a binary mask. If False (default), return a boolean mask.

		Returns
		-------
		result_mask : np.ndarray
			The output mask.
		"""
		mask_value = 0
		for value in values:
			mask_value |= value  # The |= operator is a bitwise OR assignment operator
		result_mask = (self & mask_value) > 0
		if binary and inverted:
			result_mask = result_mask.astype(int)
			result_mask = result_mask ^ 1
			return result_mask.astype(dtype)
		elif binary:
			return result_mask.astype(int)
		else:
			return result_mask.astype(dtype)

class marfits(fits.HDUList):
	"""A subclass of fits.HDUList with additional methods for handling MAR-specific FITS files.

	Attributes:
		- tabhdu: a reference to the TableHDU object associated with this FITS file.
		- _file: the name of the file associated with this FITS file.
		- hdus: a list of HDU objects associated with this FITS file.
		- filename: the name of the file associated with this FITS file.

	Methods:
		- __init__(self, hdus=[], file=None): initializes a new marfits object with optional hdus and file name parameters.
		- fromfile(cls, file, mode="copyonwrite", memmap=False, **kwargs): returns a new marfits object by reading a FITS file.
		- writeto(self, filename, compress=True, overwrite=False, usefilename=False): writes the contents of the marfits object to a new FITS file.
		- writetosingle(self, filename, compress=True, overwrite=False, usefilename=False, headerhdu=0, datahdu=1): writes the contents of the marfits object to a new FITS file with only the specified header and data HDUs.
		- updateheader(self, headerhdu=0, ignore_cards=[]): updates the header of the specified HDU with values from the MAR instrument configuration.
		- transfheader(self, startext=0, endext=1): transfers the header cards from one HDU to another.
		- setCard(self, card, value, comment='', headerhdu=0): sets a value for a specified card in the header of a specified HDU.
		- delCard(self, card, headerhdu=0): removes a specified card from the header of a specified HDU.
		- getCard(self, card, headerhdu=0): retrieves the value of a specified card from the header of a specified HDU.
		- getAmpArea(self, amp): returns the pixel coordinates for a specified amplifier area.

	Usage:
		Create a new marfits object from a FITS file:
		>>> fitsfile = marfits.fromfile('filename.fits')

		Write the contents of a marfits object to a new FITS file:
		>>> fitsfile.writeto('newfilename.fits')

		Update the header of the second HDU in the FITS file with values from the MAR instrument configuration:
		>>> fitsfile.updateheader(headerhdu=1)

		Retrieve the value of the RA card from the header of the first HDU:
		>>> ra = fitsfile.getCard('RA')
	"""
	def __init__(self, hdus=[], file=None):
		self.tabhdu = None
		self._file = file
		self.hdus = hdus
		if hdus is None:
			hdus = []

		super(marfits, self).__init__(hdus=hdus, file=file)
		self.filename = super(marfits, self).filename()

		if self.filename == None:
			try:
				self.filename = self.hdus[0]['FILENAME'].split('/')[-1]
			except:
				try:
					self.filename = self.hdus[1]['FILENAME'].split('/')[-1]
				except:
					MarManager.DEBUG('Did not find FILENAME in header.')



		configVal = mar.AttributeDict(mar.env.marConf.Instrument)

		ampSize = mar.utilities.conversion.str2coordinate(configVal['HIERARCH MAR DET OUT1 IMSC'])
		self.amps = configVal['HIERARCH MAR DET OUTPUTS']

		self.ampSize = (ampSize[1] - ampSize[0], ampSize[3] - ampSize[2])
		self.orders = np.array(mar.env.marConf.Scan['CCD_ORDER']) ## FOR SPLUS
		self.indices = np.indices(self.orders.shape)


	@classmethod
	def fromfile(cls, file, mode="copyonwrite", memmap=False, usemask=False, maskfile=None, **kwargs):
		"""
		Open a FITS file and return a `marfits` object with its HDUs.

		Parameters
		----------
		file : str
			The name of the FITS file to open.

		mode : str, optional
			The mode to use for opening the file. The options are 'readonly',
			'update', and 'copyonwrite'. Default is 'copyonwrite'.

		memmap : bool, optional
			If True, use memory mapping to access the data in the file. Default is False.

		usemask : bool, optional
			If True, loads `maskfile` FITS and append to `marfits`. Default is False.

		maskfile : str, optional
			Mask filepath. Load mask FITS file and append to the `marfits`. Default is 
			None.

		**kwargs
			Additional arguments to pass to the `fits.open` function.

		Returns
		-------
		hdus : `marfits`
			A `marfits` object containing the HDUs of the FITS file.

		"""
		# Open the file with the given mode and memmap options
		hdus = super(marfits, cls).fromfile(file, mode=mode, memmap=memmap, **kwargs)

		try:
			# Extract the filename from the full path and log a debug message
			MarManager.DEBUG('Opened ' + file)
			cls.filename = file.split('/')[-1]
		except:
			pass

		if usemask:
			_mff = False
			if maskfile is not None:
				try:
					mask = getdata(maskfile)
					_mff = True
				except:
					MarManager.DEBUG('Unable to read mask from file ' + maskfile)
				
			for key, hdu in enumerate(hdus):
				if "MASK" in hdu.name:
					hdus[key].data = MaskArray(hdu.data)
					MarManager.DEBUG('Mask HDU already exists in file ' + file)
					cls.hdus = hdus
					return hdus

			if _mff:
				MarManager.DEBUG('Creating mask HDU from file ' + maskfile)
				_tmpmask = np.array(mask, dtype='uint8')
			else:
				MarManager.DEBUG('Creating mask HDU with no masked pixels')
				_tmpmask = np.zeros(hdus[-1].data.shape, dtype='uint8')
			mask_hdu = CompImageHDU(MaskArray(_tmpmask))
			# Override HDU name
			mask_hdu_name = 'COMPRESSED_MASK'
			mask_hdu.name = mask_hdu_name
			MarManager.DEBUG('Appending mask HDU')
			hdus.append(mask_hdu)

		# Set the HDUs attribute of the `marfits` object and return it
		cls.hdus = hdus
		return hdus
	
	def add_to_mask(self, mask, value):
		for key, hdu in enumerate(self):
			if "MASK" in hdu.name:
				hdu.data.add_mask(mask, value)

	def get_mask(self, values=None, binary=False, inverted=False, dtype='uint8'):
		for key, hdu in enumerate(self):
			if "MASK" in hdu.name:
				if values is None:
					return hdu.data
				return hdu.data.get_mask(values, binary, inverted, dtype)
			
	def write_mask(self, maskfile):
		for key, hdu in enumerate(self):
			if "MASK" in hdu.name:
				hdu.writeto(maskfile, overwrite=True)

	def writeto(self, filename, compress=True, overwrite=False, usefilename=False):
		"""
		Write the HDUs of the `marfits` object to a FITS file.

		Parameters
		----------
		filename : str
			The name of the FITS file to write to.

		compress : bool, optional
			If True, compress the output file using fpack. Default is True.

		overwrite : bool, optional
			If True, overwrite any existing file with the same name. Default is False.

		usefilename : bool, optional
			If True, use the `filename` attribute of the `marfits` object as the name
			of the output file. Default is False.

		Returns
		-------
		None

		"""
		if usefilename:
			# Use the filename attribute of the `marfits` object as the output filename
			filename = self.filename

		# Write the HDUs to the output file
		super(marfits, self).writeto(filename, overwrite=overwrite)

		if compress:
			# Compress the output file using fpack
			res = os.system('fpack ' + filename)
			if res != 0:
				MarManager.WARN('Fpack compression failed')
			if res == 0:
				# Remove the original file if the compression was successful
				os.system('rm ' + filename)

		return

	def writetosingle(self, filename, compress=True, overwrite=False, usefilename=False, headerhdu=0, datahdu=1):
		"""
		Write a single HDU of the `marfits` object to a FITS file.

		Parameters
		----------
		filename : str
			The name of the FITS file to write to.

		compress : bool, optional
			If True, compress the output file using fpack. Default is True.

		overwrite : bool, optional
			If True, overwrite any existing file with the same name. Default is False.

		usefilename : bool, optional
			If True, use the `filename` attribute of the `marfits` object as the name
			of the output file. Default is False.

		headerhdu : int, optional
			The index of the HDU containing the header to write to the output file. Default is 0.

		datahdu : int, optional
			The index of the HDU containing the data to write to the output file. Default is 1.

		Returns
		-------
		None

		"""
		if usefilename:
			# Use the filename attribute of the `marfits` object as the output filename
			filename = self.filename

		# Transform the HDU header to the desired format
		if datahdu == 1:
			self.transfheader(1, 0)

		# Create a new `marfits` object with the desired HDU and write it to the output file
		nhdu = marfits([fits.PrimaryHDU(header=self[headerhdu].header, data=self[datahdu].data)])
		nhdu.writeto(filename, overwrite=overwrite, compress=compress, usefilename=usefilename)

		return


	def updateheader(self, headerhdu=0, ignore_cards=[]):
		"""
		Update the header of an HDU of the `marfits` object with instrument configuration.

		Parameters
		----------
		headerhdu : int, optional
			The index of the HDU containing the header to update. Default is 0.

		ignore_cards : list of str, optional
			A list of header cards to ignore when updating the header. Default is an
			empty list.

		Returns
		-------
		`marfits`
			A new `marfits` object with the updated header.

		"""
		try:
			# Load the instrument configuration
			instrument = AttributeDict(env.marConf.Instrument)
		except:
			MarManager.CRITICAL('Intrument config not found.')
			raise ValueError("Intrument config not found.")

		# Create a dictionary of the header cards and their values to update
		values = instrument
		ignore_cards = ["SIMPLE", "BITPIX", "EXTEND", "EXTENSION"] + ignore_cards

		# Update the header cards with the values from the instrument configuration
		for card in values.keys():
			if (card in ignore_cards):
				continue
			elif card in self[headerhdu].header.keys() and card not in ["HISTORY", "COMMENT", ""]:
				# If the card is already in the header, set its value to the new value
				self[headerhdu].header.set(card, values[card])
			else:
				# If the card is not in the header, append it to the header with the new value
				self[headerhdu].header.append((card, values[card]))

		MarManager.INFO('Updated header ' + self.filename)
		return self


	def transfheader(self, startext=0, endext=1):
		"""
		Transfer header information from one HDU to another in the `marfits` object.

		Parameters
		----------
		startext : int, optional
			The index of the source HDU to transfer header information from. Default is 0.

		endext : int, optional
			The index of the destination HDU to transfer header information to. Default is 1.

		Returns
		-------
		None
		"""

		for card in self[startext].header.cards:
			if (card.keyword in ["SIMPLE", "BITPIX", "EXTEND", "EXTENSION", "NAXIS","NAXIS2", "NAXIS1"]):
				continue
			elif card.keyword in self[endext].header.keys() and card.keyword not in ["HISTORY", "COMMENT", ""]:
				self[endext].header.set(card.keyword, card.value, card.comment)
			else:
				self[endext].header.append(card)


	def setCard(self, card, value, comment='', headerhdu=0):
		"""
		Set the value of a specific header card in an HDU of the `marfits` object.

		Parameters
		----------
		card : str
			The name of the header card to set.

		value : object
			The new value for the header card.

		comment : str, optional
			A comment to add to the header card. Default is an empty string.

		headerhdu : int, optional
			The index of the HDU containing the header to update. Default is 0.

		Returns
		-------
		None
		"""

		card = card.upper()

		if (card in ["SIMPLE", "BITPIX", "EXTEND", "EXTENSION"]):
			return
		elif card in self[headerhdu].header.keys() and card not in ["HISTORY", "COMMENT", ""]:
			self[headerhdu].header.set(card, value, comment)
		else:
			self[headerhdu].header.append((card, value, comment))


	def delCard(self, card, headerhdu=0):
		"""
		Delete a specific header card in an HDU of the `marfits` object.

		Parameters
		----------
		card : str
			The name of the header card to delete.

		headerhdu : int, optional
			The index of the HDU containing the header to delete the card from. Default is 0.

		Returns
		-------
		None
		"""

		card = card.upper()
		del self[headerhdu].header[card]


	def getCard(self, card, headerhdu=0):
		"""
		Get the value of a specific header card in an HDU of the `marfits` object.

		Parameters
		----------
		card : str
			The name of the header card to get the value of.

		headerhdu : int, optional
			The index of the HDU containing the header to get the card value from. Default is 0.

		Returns
		-------
		object or bool
			The value of the specified header card if it exists in the HDU header, else `False`.
		"""

		card = card.upper()
		try:
			return self[headerhdu].header[card]
		except:
			return False

	def getAmpArea(self, amp):
		y = self.indices[0][(self.orders == amp)][0]
		x = self.indices[1][(self.orders == amp)][0]

		image_section = [y * self.ampSize[0], (y + 1) * self.ampSize[0], x * self.ampSize[1], (x + 1) * self.ampSize[1]]
		return image_section









# file = marfits.fromfile(file='/Users/gustavo/Documents/t80testblock/FLAT/skyflat-20210117-002847.fits.fz', usemask=True)
# file.writeto('/Users/gustavo/Documents/salve.fits', overwrite=True)


def getAmpArea(amp):
	"""
	Returns the image section of the given amplifier.

	Parameters
	----------
	amp : int
		The amplifier number.

	Returns
	-------
	list
		The image section of the given amplifier.
	"""
	configVal = mar.AttributeDict(mar.env.marConf.Instrument)

	ampSize = mar.utilities.conversion.str2coordinate(configVal['HIERARCH MAR DET OUT1 IMSC'])
	amps = configVal['HIERARCH MAR DET OUTPUTS']

	ampSize = (ampSize[1] - ampSize[0], ampSize[3] - ampSize[2])
	orders = np.array(mar.env.marConf.Scan['CCD_ORDER']) ## FOR SPLUS
	indices = np.indices(orders.shape)

	y = indices[0][(orders == amp)][0]
	x = indices[1][(orders == amp)][0]

	image_section = [y * ampSize[0], (y + 1) * ampSize[0], x * ampSize[1], (x + 1) * ampSize[1]]
	return image_section


