import mar

from astropy.io import fits
from astropy.table import Table, vstack
import numpy as np

from mar.wrappers import *

from mar.config import MarManager

class SExtractorCatalog(SExtr):
	"""Class that runs Sextractor with some defined values in config. 
	The goal here is to run a simple catalog to detect objects and some parameters.

	Args:
		SExtr (mar.wrappers.SExtr): Sextractor wrapper.
	"""
	def __init__(self, image, mask=None, winparams=True, folder='/tmp', catname="catout.param"):
		SExtr.__init__(self, image=image, folder=folder, catname=catname)

		MarManager.INFO("Starting SExtractor Class.")
		self.marConf = mar.AttributeDict(mar.env.marConf.Reduction)
		self.config['BACK_FILTERSIZE']['value'] = self.marConf.CAT_BACK_FILTERSIZE
		self.config['BACK_SIZE']['value'] = self.marConf.CAT_BACK_SIZE
		self.config['DETECT_THRESH']['value'] = self.marConf.CAT_DETECT_THRESH
		self.config['ANALYSIS_THRESH']['value'] = self.marConf.CAT_DETECT_THRESH
		self.config['DETECT_MINAREA']['value'] = self.marConf.CAT_DETECT_MINAREA


		self.config['WEIGHT_TYPE']['value'] = "NONE"
		self.config['CHECKIMAGE_TYPE']['value'] = 'SEGMENTATION, BACKGROUND, BACKGROUND_RMS'
		self.config['CLEAN']['value'] = "Y"

		if mask is not None:
			self.config['WEIGHT_TYPE']['value'] = 'MAP_WEIGHT'
			self.config['WEIGHT_IMAGE']['value'] = mask
			self.config['WEIGHT_THRESH']['value'] = 0

		self.config['CHECKIMAGE_TYPE']['value'] = 'NONE'

		self.params = [
			'NUMBER', 'X_IMAGE', 'Y_IMAGE',
			'THETA_WORLD', 'ERRTHETA_WORLD',
			'ERRA_IMAGE', 'ERRB_IMAGE',
			'ERRTHETA_IMAGE',
			'FLUX_AUTO', 'FLUXERR_AUTO', 'ALPHA_J2000', 'DELTA_J2000',
			'X_WORLD', 'Y_WORLD',
			'MAG_AUTO', 'MAG_BEST', 'MAGERR_AUTO',
			'MAGERR_BEST', 'FLUX_MAX', 'FWHM_IMAGE', 'FLAGS',
			'ELLIPTICITY',
			'MU_THRESHOLD', 'THRESHOLD', 'BACKGROUND', 'THETA_IMAGE',
			'A_IMAGE', 'B_IMAGE',
			'FLUX_RADIUS',
			'ISOAREA_IMAGE']

		if winparams:
			self.params.extend([
					'XWIN_IMAGE', 'YWIN_IMAGE',
					'ERRAWIN_IMAGE', 'ERRBWIN_IMAGE',
					'ERRTHETAWIN_IMAGE'])


		def run(self):
			MarManager.INFO("Running SExtractor.")
			self.run()


class CatalogOperation:
	def __init__(self, catalog):
		"""Instantiate class with catalog path name. 

		Args:
			catalog (str): file path.
		"""
		self.table = fits.open(catalog)
		self.catalog = Table(self.table[2].data)
		self.marConf = mar.AttributeDict(mar.env.marConf.Reduction)

	def stars(self, distributed=False, do_selection=True):
		"""Function to calculate inicial seeing FWHM, and some stats from given catalog. 
		"""		
		MarManager.INFO("Calculating 'seeing' FWHM and stats from catalog.")

		magerrmax = 1.0857 / self.marConf.FWHM_SNmin
		self.catalog['SNR'] = self.catalog['FLUX_AUTO'] / self.catalog['FLUXERR_AUTO']
		
		if do_selection:
			selection = (
			 	 (self.catalog["FLAGS"] == 0) &
			 	 (self.catalog["ELLIPTICITY"] < self.marConf.FWHM_ELLIPMAX) &
			 	 (self.catalog["ISOAREA_IMAGE"] > self.marConf.FWHM_ISOAREAMIN) &
			 	 (self.catalog["MAGERR_AUTO"] < magerrmax) &
			 	 (self.catalog["SNR"] < self.marConf.MAX_SNR)
			)
		
		else:
			selection = (
				(self.catalog["FLAGS"] == 0)
			)		
		
		self.catalogStars = self.catalog[selection]
		self.catalogStars.sort('MAGERR_AUTO')
		
		self.stats = mar.utilities.robustStat(self.catalogStars[0:150]['FWHM_IMAGE'])
		self.FWHMSEXT = self.stats['median'] * self.marConf.PIXSCALE
		if not self.stats['rms']:
			self.stats['rms'] = 0
			MarManager.WARN("Invalid FWHMSRMS (rms - NoneType)")
		self.FWHMSRMS = self.stats['rms'] * self.marConf.PIXSCALE
		
		if distributed:
			try: self.catalogStars = get_distributed_objects(self.catalogStars)
			except: MarManager.WARN("Unable to distribute stars over image. Astrometry may be affected")
			
	def saveStarsCatalog(self, path, overwrite=True):
		"""Function to save stars catalog. Used to give to scamp. 
		"""
		MarManager.INFO("Saving stars catalog.")
		self.table[2].data = np.array(self.catalogStars)
		self.table.writeto(path, overwrite=overwrite)


def get_distributed_objects(catalog, n_grid=None, objects_per_cell=None, margin=None):
	"""
	Selects a uniform distribution of objects from a SExtractor catalog grid.

	Parameters
	----------
	catalog : astropy.table.Table
		The input SExtractor catalog.
	n_grid : int, optional
		The number of cells along each axis of the grid. The total number of cells is n_grid*n_grid. 
		Default is 10.
	objects_per_cell : int, optional
		The maximum number of objects to select from each cell. The function will select this number 
		of objects from all cells, unless some cells have fewer than this number of objects but more 
		than the specified margin. Default is 1.
	margin : int, optional
		The minimum number of objects that a cell must have in order to influence the total number of 
		objects selected from all cells. If a cell has fewer than this number of objects, the function 
		will still select objects_per_cell objects from all other cells. Default is 5.

	Returns
	-------
	distributed_objects : astropy.table.Table
		A table of the selected objects.

	Notes
	-----
	The function selects objects based on their X_IMAGE and Y_IMAGE values. It divides the image into 
	a grid of cells, then selects a uniform number of objects from each cell. The number of objects 
	selected from each cell is the smaller of objects_per_cell and the number of objects in the cell 
	with the smallest number of objects (provided that number is greater than or equal to the margin). 
	The selected objects are those with the smallest MAGERR_AUTO values.

	Examples
	--------
	>>> from astropy.table import Table
	>>> import numpy as np
	>>> catalog = Table({'X_IMAGE': np.random.rand(100), 'Y_IMAGE': np.random.rand(100), 'MAGERR_AUTO': np.random.rand(100)})
	>>> distributed_objects = get_distributed_objects(catalog, n_grid=5, objects_per_cell=2, margin=1)
	"""
	marConf = mar.AttributeDict(mar.env.marConf.Reduction)
	if n_grid is None:
		n_grid = int(marConf.CAT_NGRID)
	
	if objects_per_cell is None:
		objects_per_cell = int(marConf.OBJECTS_PER_CELL)
		
	if margin is None:
		margin = int(marConf.CAT_MARGIN)

	# Get the bounds of the image
	x_min, x_max = np.min(catalog['X_IMAGE']), np.max(catalog['X_IMAGE'])
	y_min, y_max = np.min(catalog['Y_IMAGE']), np.max(catalog['Y_IMAGE'])

	# Compute the size of each cell
	x_size = (x_max - x_min) / n_grid
	y_size = (y_max - y_min) / n_grid

	# Initialize the minimum number of stars per cell to a large value
	min_stars_per_cell = objects_per_cell

	# Iterate over the cells to find the minimum number of stars per cell
	for i in range(n_grid):
		for j in range(n_grid):
			# Get the bounds of the current cell
			x_cell_min = x_min + i * x_size
			x_cell_max = x_min + (i + 1) * x_size
			y_cell_min = y_min + j * y_size
			y_cell_max = y_min + (j + 1) * y_size

			# Count the objects in the current cell
			objects_in_cell = catalog[(catalog['X_IMAGE'] >= x_cell_min) & (catalog['X_IMAGE'] < x_cell_max) &
									  (catalog['Y_IMAGE'] >= y_cell_min) & (catalog['Y_IMAGE'] < y_cell_max)]

			# Update the minimum number of stars per cell if the number of stars in the cell is greater than the margin
			if len(objects_in_cell) >= margin:
				min_stars_per_cell = min(min_stars_per_cell, len(objects_in_cell))

	# Initialize distributed_objects as an empty Table
	distributed_objects = Table()

	# If no cell has enough stars, raise an exception
	if min_stars_per_cell < 1:
		MarManager.WARN('Not enough stars in some cells.')

	# Iterate over the cells again to select stars
	for i in range(n_grid):
		for j in range(n_grid):
			# Get the bounds of the current cell
			x_cell_min = x_min + i * x_size
			x_cell_max = x_min + (i + 1) * x_size
			y_cell_min = y_min + j * y_size
			y_cell_max = y_min + (j + 1) * y_size

			# Select the objects in the current cell
			objects_in_cell = catalog[(catalog['X_IMAGE'] >= x_cell_min) & (catalog['X_IMAGE'] < x_cell_max) &
									  (catalog['Y_IMAGE'] >= y_cell_min) & (catalog['Y_IMAGE'] < y_cell_max)]

			# Sort the objects by MAGERR_AUTO
			objects_in_cell.sort("MAGERR_AUTO")

			# Select the top min_stars_per_cell objects and add them to distributed_objects
			chosen_objects = objects_in_cell[:min_stars_per_cell]
			distributed_objects = vstack([distributed_objects, chosen_objects])

	return distributed_objects


"""
sextr = mar.reduction.SExtractorCatalog('/home/ubuntu/Home/Documents/swarp/UHcoadded.fits', folder='/home/ubuntu/Home/Documents/SExtr')
sextr.run()

info = mar.reduction.CatalogOperation('/home/ubuntu/Home/Documents/SExtr/catout.param')
info.stars()

hdu = mar.image.marfits.fromfile('/home/ubuntu/Home/Documents/swarp/UHcoadded.fits', mode="update")

hdu.setCard('MAR PRO FWHMSEXT', info.FWHMSEXT)
hdu.setCard('MAR PRO FWHMSRMS', info.FWHMSRMS)

hdu.flush()
"""
