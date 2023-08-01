from astropy.io import fits
from astropy.stats import sigma_clip
import numpy as np
import os

import gc
from mar.image.fits import marfits

import warnings

warnings.filterwarnings("ignore", message="Keyword name")
warnings.filterwarnings("ignore", message="Input data contains")

from mar import env, AttributeDict

from mar.utilities import stats, conversion
from scipy.interpolate import UnivariateSpline
from scipy.signal import medfilt

marconfig = AttributeDict(env.marConf.Scan)

from scipy.interpolate import interp1d
from scipy import ndimage

from mar.config import MarManager


class Scan:
    """Class for overscan and prescan correction of an image

    Args:
        filename (str, optional): The name of the file to be corrected. Defaults to None.
        hdu (HDUList, optional): The HDUList of the file to be corrected. Defaults to None.
        dmean (bool, optional): Set to True to calculate the mean of the image. Defaults to False.
    """

    def __init__(self, filename=None, hdu=None, dmean=False):
        '''
		hdu must be marfits HDUList instance (Opened with fromfile method).
		'''

        # Set default values for the various correction parameters
        self.makeovsc = marconfig.USE_OVERSCAN
        self.makepresc = marconfig.USE_PRESCAN

        self.ovscx = marconfig.USE_OVERSCAN_X
        self.ovscy = marconfig.USE_OVERSCAN_Y

        self.prescx = marconfig.USE_OVERSCAN_Y
        self.prescy = marconfig.USE_PRESCAN_Y

        self.direction = marconfig.DIRECTION
        self.xfit = marconfig.FITFUNCTION_X
        self.yfit = marconfig.FITFUNCTION_Y
        self.polydegx = marconfig.POLYDEG_X
        self.polydegy = marconfig.POLYDEG_Y
        self.superpixelsizex = marconfig.OVSC_NPIXELS_X
        self.superpixelsizey = marconfig.OVSC_NPIXELS_Y
        self.xcorrect = marconfig.XCORRECT

        # Determine whether or not to calculate the mean of the image
        self.doxmean = False

        self.interpolatorx = marconfig.OVERSCAN_INTERPOLATION_METHOD_X
        self.interpolatory = marconfig.OVERSCAN_INTERPOLATION_METHOD_Y

        self.fitfunctionx = marconfig.FITFUNCTION_X
        self.fitfunctiony = marconfig.FITFUNCTION_Y

        self.sspixels = None

        self.areas = [False, False, False, False]  # ovscX, ovscY, prescX, prescY

        # Load in the file and the HDUList
        if filename != None:
            self.filename = filename
            self.hdu = marfits.fromfile(filename)

            self.hdu.updateheader()

        elif hdu != None:
            self.hdu = marfits(hdus=hdu)

        if not self.makeovsc:
            (self.ovscx, self.ovscy) = False, False
        if not self.makepresc:
            (self.prescx, self.prescy) = False, False

    def run(self, headerHDU=0, dataHDU=1, trim=True):
        if self.hdu.getCard('OVERSCAN'):
            print('Ovsc already applied')

        nAMP = self.hdu[headerHDU].header["HIERARCH MAR DET OUTPUTS"]

        try:
            MarManager.INFO('Running overscan correction on file: ' + self.filename)
        except: pass

        try:
            self.hdu[dataHDU]
        except:
            dataHDU = 0
        
        print(dataHDU, self.hdu)
        for amp in range(1, nAMP + 1):
            self.get_areas(amp, headerHDU)
            if True in self.areas:
                for direction in self.direction:
                    if direction != 'x' and direction != 'y':
                        raise Exception('Direction not recognized. (must be x or y)')

                    self.calculate_offset(direction=direction, dataHDU=dataHDU)
                    self.apply_subtraction(dataHDU=dataHDU)

        if trim:
            MarManager.INFO('Overscan done, applying trim')
            self.trim(dataHDU=dataHDU, headerHDU=headerHDU)
            self.hdu.setCard('OVERSCAN', True, 'Applied Overscan and Trim')
        else:
            self.hdu.setCard('OVERSCAN', True, 'Applied Overscan')


    def calculate_offset(self, direction, dataHDU):
        """Calculates the overscan or prescan offset values in the input image, depending on the value of the direction argument. This method is used internally by the run method to correct for overscan and prescan areas of the input image.

        Args:

        self (object): the Scan object itself.
        direction (str): The direction to perform the calculation ('x' or 'y').
        dataHDU (int): The index of the HDU in which the data is stored.
        Returns:

        None
        The method calculates the overscan or prescan offset by first calculating the median or mean of the overscan or prescan areas of the input image. The method then interpolates over bad pixels and clips outliers to arrive at a corrected overscan or prescan offset. The method then saves the overscan or prescan offset values in the offset attribute of the Scan object, depending on the value of the direction argument.
        """        
        self.overscan_data = None
        self.prescan_data = None
        nsplit = None

        if True in self.areas:
            self.ovscx_data = None
            self.ovscy_data = None
            self.prscx_data = None
            self.prscy_data = None

            if self.ovscx_area is not None and self.ovscx:
                if self.xcorrect:
                    self.ovscx_data = self.hdu[dataHDU].data[self.ovscx_area[0]:self.ovscx_area[1],
                                      self.ovscx_area[2]:self.ovscx_area[3]].copy()
                else:
                    self.ovscx_data = self.hdu[dataHDU].data[self.ovscx_area[0]:self.ovscx_area[1],
                                      self.imsc_area[2]:self.imsc_area[3]].copy()

            if self.ovscy_area is not None and self.ovscy:
                if self.xcorrect:
                    self.ovscy_data = self.hdu[dataHDU].data[self.ovscy_area[0]:self.ovscy_area[1],
                                      self.ovscy_area[2]:self.ovscy_area[3]]
                else:
                    self.ovscy_data = self.hdu[dataHDU].data[self.imsc_area[0]:self.imsc_area[1],
                                      self.ovscy_area[2]:self.ovscy_area[3]]

            if self.prscx_area is not None and self.prescx:
                if self.xcorrect:
                    self.prscx_data = self.hdu[dataHDU].data[self.prscx_area[0]:self.prscx_area[1],
                                      self.prscx_area[2]:self.prscx_area[3]]
                else:
                    self.prscx_data = self.hdu[dataHDU].data[self.prscx_area[0]:self.prscx_area[1],
                                      self.imsc_area[2]:self.imsc_area[3]]

            if self.prscy_area is not None and self.prescy:
                if self.xcorrect:
                    self.prscy_data = self.hdu[dataHDU].data[self.prscy_area[0]:self.prscy_area[1],
                                      self.prscy_area[2]:self.prscy_area[3]]
                else:
                    self.prscy_data = self.hdu[dataHDU].data[self.imsc_area[0]:self.imsc_area[1],
                                      self.prscy_area[2]:self.prscy_area[3]]

            overscan = []
            prescan = []
            pix_pos = []

            if direction == 'x':
                self.over = self.ovscx
                self.pres = self.prescx

                self.interpmethod = self.interpolatorx
                self.fixbadpixcol = marconfig.OVERSCAN_FIX_BAD_PIXELS_COLUMNS_X
                self.fixbadpix = marconfig.OVERSCAN_CORRECT_IND_PIXELS_X
                self.sspixels = self.superpixelsizex

                self.polydeg = self.polydegx
                self.fitfunction = self.fitfunctionx

                if self.ovscx:
                    self.overscan_data = self.ovscx_data.T
                    shape = self.overscan_data.shape

                if self.prescx:
                    self.prescan_data = self.prscx_data.T
                    shape = self.prescan_data.shape

            if direction == 'y':
                self.over = self.ovscy
                self.pres = self.prescy

                self.interpmethod = self.interpolatory
                self.fixbadpixcol = marconfig.OVERSCAN_FIX_BAD_PIXELS_COLUMNS_Y
                self.fixbadpix = marconfig.OVERSCAN_CORRECT_IND_PIXELS_Y
                self.sspixels = self.superpixelsizey

                self.polydeg = self.polydegy
                self.fitfunction = self.fitfunctiony

                if self.ovscy:
                    self.overscan_data = self.ovscy_data.T
                    del self.ovscy_data
                    shape = self.overscan_data.shape

                if self.prescy:
                    self.prescan_data = self.prscy_data.T
                    del self.prscy_data
                    shape = self.prescan_data.shape
                    gc.collect()

            if self.fixbadpixcol and self.over:
                ovsc_med = stats.mean_robust(self.overscan_data, axis=1)

                _, ovsclow, ovscup = sigma_clip(ovsc_med, sigma=5, maxiters=1, stdfunc=stats.MAD, cenfunc='median',
                                                return_bounds=True)

                badpix = (ovsc_med > ovscup) | (ovsc_med < ovsclow)
                self.ovbadpix_index = np.where(badpix)[0]

                structure = ndimage.generate_binary_structure(1, 1)
                badpix = ndimage.binary_dilation(badpix, structure=structure, iterations=10)
                goodpix = np.logical_not(badpix)

                self.ovbadpix_index = np.where(badpix)[0]
                indexes = np.arange(ovsc_med.shape[0])
                goodpix_index = np.where(goodpix)[0]
                medianval = np.median(np.array(ovsc_med[goodpix_index]))

                if self.interpmethod == "medianvalue":
                    res = np.where(goodpix, self.overscan_data.transpose(), medianval)

                if self.interpmethod == "linearinterp":
                    f = interp1d(goodpix_index, ovsc_med[goodpix_index], axis=0, bounds_error=False,
                                 fill_value=medianval)
                    res = np.where(goodpix, self.overscan_data.transpose(), f(indexes).transpose())

                if self.interpmethod == "medianfilter":
                    masked_overscan = np.ma.array(ovsc_med, mask=badpix)
                    filteredvals = medianfilter1d(masked_overscan, 101)
                    res = np.where(goodpix, self.overscan_data.transpose(), filteredvals)

                self.overscan_data = res.transpose()

                if self.fixbadpix:
                    self.overscan_data = np.apply_along_axis(stats.interpolate, 0, self.overscan_data, 5)

            if self.sspixels is None:
                if self.over:
                    overscan = np.mean(self.overscan_data, axis=1)
                    if self.fixbadpixcol:
                        auxov, cl, cu = sigma_clip(overscan, sigma=5, maxite=1, stdfunc=stats.MAD, cenfunc='median',
                                                   return_bounds=True)
                        badpix = np.where((overscan > cu) | (overscan < cl))[0]

                        indexes = np.arange(overscan.shape[0])
                        goodpix = np.where((overscan <= cu) & (overscan >= cl))[0]

                        medianval = np.median(overscan[goodpix])
                        f = interp1d(indexes[goodpix], overscan[goodpix], bounds_error=False, fill_value=medianval)
                        overscan = np.where((overscan <= cu) & (overscan >= cl), overscan, f(indexes))

                if self.pres:
                    prescan = stats.mean_robust(self.prescan_data, axis=1)

                pix_pos = np.arange(shape[0])
                self.sspixels = 1
                nsplit = len(pix_pos)

            if self.sspixels is not None:
                for i in range(np.floor_divide(shape[0], self.sspixels) - 1):
                    pos = (i * self.sspixels, (i + 1) * self.sspixels)

                    if self.over:
                        if self.doxmean:
                            aax = np.mean(self.overscan_data[pos[0]: pos[1], :], axis=0, dtype=np.float64)
                        else:
                            aax = self.overscan_data[pos[0]:pos[1], :]

                        if self.fixbadpixcol:
                            aax = np.where((aax > ovscup), ovscup, aax)
                            aax = np.where((aax < ovsclow), ovsclow, aax)
                        overscan.append(stats.mean_robust(np.array(aax, dtype=np.float64)))

                    if self.pres:
                        if self.doxmean:
                            aax = np.mean(self.prescan_data[pos[0]:pos[1], :], axis=0, dtype=np.float64)
                        else:
                            aax = self.prescan_data[pos[0]:pos[1], :].ravel()

                        prescan.append(stats.mean_robust(np.array(aax, dtype=np.float64)))
                        prescan = np.array(prescan)

                    pix_pos.append((i + 0.5) * self.sspixels)

                pos = shape[0] - self.sspixels
                if self.over:
                    if self.doxmean:
                        aax = np.mean(self.overscan_data[pos:, :], axis=0, dtype=np.float64)
                    else:
                        aax = self.overscan_data[pos:, :].ravel()

                    if self.fixbadpixcol:
                        aax = np.where(aax > ovscup, ovscup, aax)
                    overscan.append(stats.mean_robust(np.array(aax, dtype=np.float64)))
                    overscan = np.array(overscan)

                if self.pres:
                    if self.doxmean:
                        aax = np.mean(self.prescan_data[pos:, :], axis=0, dtype=np.float64)

                    else:
                        aax = self.prescan_data[pos:, :].ravel()

                    prescan.append(stats.mean_robust(np.array(aax, np.float64)))
                    prescan = np.array(prescan)

                pix_pos.append(0.5 * (shape[0] + pos))
                nsplit = len(pix_pos)

            self.overscan = overscan
            self.prescan = prescan
            self.pix_pos = pix_pos
            self.npixels = self.sspixels
            self.nsplit = nsplit

            if self.over and not self.pres:
                self.offset = self.overscan
            elif self.pres and not self.over:
                self.offset = self.prescan

            elif self.pres and self.over:
                self.offset = (self.prescan + self.overscan) / 2

            del self.overscan_data, self.prescan_data
            gc.collect()

    def apply_subtraction(self, dataHDU, applytohdu=True):
        """
        Applies the overscan or prescan subtraction to the specified HDU data in-place, and returns the modified data.

        Args:
            dataHDU (int): The HDU index of the data to be corrected in the FITS file.
            applytohdu (bool): Whether to modify the data in the HDU of the FITS file (default True).

        Returns:
            numpy.ndarray: The corrected data, after subtracting the calculated overscan or prescan value.

        Raises:
            Exception: If the shapes of the image and correction area do not match.

        The correction is performed by subtracting the calculated overscan or prescan value from the data within the image area,
        obtained from the data in the correction area previously defined by `calculate_offset()`.
        The method supports three types of fitting functions for the overscan/prescan correction: polynomial, spline, and median filter.
        The type of function used is specified by the `fitfunction` attribute of the Scan object.
        If the `applytohdu` parameter is set to True (default), the modified data is written back to the original HDU.
        The image area is defined by the `imsc_area` attribute of the Scan object, and correction areas are defined by
        `ovscx_area`, `ovscy_area`, `prscx_area`, `prscy_area`, and `direction` attributes.
        """
        area = self.imsc_area.copy()
        if self.xcorrect:
            for reg in [self.ovscx_area, self.ovscy_area, self.prscx_area, self.prscy_area]:
                if reg is not None:
                    area[0] = min(area[0], reg[0])
                    area[1] = max(area[1], reg[1])
                    area[2] = min(area[2], reg[2])
                    area[3] = max(area[3], reg[3])

        data = self.hdu[dataHDU].data[area[0]:area[1], area[2]:area[3]].copy()

        if self.direction == 'x' or self.direction == 'yx':
            data = data.T

        if self.fitfunction == "polynomial":
            self.polinom = np.polyfit(self.pix_pos, self.offset, deg=self.polydeg)
            data = data.T - np.polyval(self.polinom, np.arange(data.shape[0]))

        elif self.fitfunction == "spline":
            self.polinom = UnivariateSpline(self.pix_pos, self.offset,
											k=self.polydeg,
											# s=len(self.pix_pos) / 2.,
											s=len(self.pix_pos))
            data = data.T - self.polinom(np.arange(data.shape[0]))

        elif self.fitfunction == "medianfilter":
            self.offsetfilter = medfilt(self.offset, kernelsize)
            if data.shape[0] != self.offsetfilter.shape[0]:
                raise Exception("Shapes of the image and correction area dont match")
            else:
                print("Removing shape " + str(self.offsetfilter.shape))
                data = data.T - self.offsetfilter

        if applytohdu:
            self.hdu[dataHDU].data[area[0]:area[1], area[2]:area[3]] = data

    def trim(self, headerHDU, dataHDU, compress=False):
        """Trims a multi-output MAR CCD image and updates headers to reflect the trimmed size.
    
        Args:
            headerHDU (int): The index of the header HDU of the input data in the `Scan.hdu` attribute.
            dataHDU (int): The index of the data HDU of the input data in the `Scan.hdu` attribute.
            compress (bool, optional): Whether to compress the trimmed data array. Defaults to False.
            
        Returns:
            None
        
        Raises:
            None
            
        The method trims a multi-output MAR CCD image by extracting subarrays from the input data
        array defined by the sub-regions specified in the headers of the image.
        The method then updates the headers of the image to reflect the new trimmed size.
        The method takes as input the indices of the header and data HDUs in the `Scan.hdu` attribute.
        The `compress` argument can be set to True to compress the trimmed data array, but this functionality
        is currently commented out and has no effect.

        """        
        imarea = conversion.str2coordinate(self.hdu[headerHDU].header['HIERARCH MAR DET OUT1 IMSC'])
        sizeamp = (imarea[1] - imarea[0], imarea[3] - imarea[2])

        order = np.array(marconfig.CCD_ORDER)
        shape = (order.shape[0] * sizeamp[0], order.shape[1] * sizeamp[1])

        outs = self.hdu[headerHDU].header["HIERARCH MAR DET OUTPUTS"]
        indices = np.indices(order.shape)

        datatrimmed = np.empty(shape)

        shape = {'x': 0, 'y': 0}
        
        for i in range(1, (outs + 1), 1):
            key = "HIERARCH MAR DET OUT" + str(i) + " IMSC"
            imarea = conversion.str2coordinate(self.hdu[headerHDU].header[key])

            x = indices[1][(order == i)][0]
            y = indices[0][(order == i)][0]

            value = conversion.coordinate2str([y * sizeamp[0], (y + 1) * sizeamp[0],
                                               x * sizeamp[1], (x + 1) * sizeamp[1]])

            imsc_area = conversion.str2coordinate(self.hdu[headerHDU].header[key])
            
            self.hdu[dataHDU].data[y * sizeamp[0]: (y + 1) * sizeamp[0],
            x * sizeamp[1]: (x + 1) * sizeamp[1]] = \
                self.hdu[dataHDU].data[imsc_area[0]:imsc_area[1],
                imsc_area[2]:imsc_area[3]]  

            shape['x'] += ((x + 1) * sizeamp[1] - x * sizeamp[1])
            shape['y'] += ((y + 1) * sizeamp[0] - y * sizeamp[0])

            self.hdu[headerHDU].header.set(keyword=key, value=value)
            self.hdu[headerHDU] = fits.PrimaryHDU(header=self.hdu[headerHDU].header, data=self.hdu[dataHDU].data)
            self.hdu[headerHDU].header.append(('DATASEC', f'[1: {datatrimmed.shape[1]}, 1: {datatrimmed.shape[0]}]'))
            
        # if not compress:
        #	hdudata = fits.ImageHDU(data=datatrimmed, header=self.hdu[dataHDU].header)
        #	self.hdu[dataHDU] = hdudata
        # else:
        #	self.hdu[dataHDU].data = datatrimmed
        if len(marconfig['CCD_ORDER']) > 1:
            shape['x'] = shape['x'] / len(marconfig['CCD_ORDER'])

            if len(marconfig['CCD_ORDER'][0]) > 1:
                shape['y'] = shape['y'] / len(marconfig['CCD_ORDER'][0])

        self.hdu[dataHDU].data = self.hdu[dataHDU].data[0:int(shape['y']), 0: int(shape['x'])]
        hdudata = None
        datatrimmed = None
        gc.collect()

    def get_areas(self, amp, headerHDU):
        """
        Retrieves the values of the amplifiers inside header keywords from the HDU in order to identify and store the positions of 
        certain areas of interest within an image.
        
        Parameters:
        -----------
        amp : int or str
            The amplifier number or label.
        headerHDU : int
            The index of the HDU containing the image header.
        """
        key_ovsc_x = "OVSCY"
        key_ovsc_y = "OVSCX"

        key_prsc_x = "PRSCY"
        key_prsc_y = "PRSCX"

        self.ovscx_area = None
        self.ovscy_area = None
        self.prscx_area = None
        self.prscy_area = None

        amp = str(amp)
        try:
            self.ovscx_area = conversion.str2coordinate(
                self.hdu[headerHDU].header['HIERARCH MAR DET OUT' + amp + " " + key_ovsc_x])
            self.areas[0] = True
        except:
            pass
        # MarManager.DEBUG("Header key " + 'HIERARCH MAR DET OUT' + amp + " " + key_ovsc_x + " not found")

        try:
            self.ovscy_area = conversion.str2coordinate(
                self.hdu[headerHDU].header['HIERARCH MAR DET OUT' + amp + " " + key_ovsc_y])
            self.areas[1] = True
        except:
            pass
        # MarManager.DEBUG("Header key " + 'HIERARCH MAR DET OUT' + amp + " " + key_ovsc_y + " not found")

        try:
            self.prscx_area = conversion.str2coordinate(
                self.hdu[headerHDU].header['HIERARCH MAR DET OUT' + amp + " " + key_prsc_x])
            self.areas[2] = True
        except:
            pass
        # MarManager.DEBUG("Header key " + 'HIERARCH MAR DET OUT' + amp + " " + key_prsc_x + " not found")

        try:
            self.prscy_area = conversion.str2coordinate(
                self.hdu[headerHDU].header['HIERARCH MAR DET OUT' + amp + " " + key_prsc_y])
            self.areas[3] = True
        except:
            pass
        # MarManager.DEBUG("Header key " + 'HIERARCH MAR DET OUT' + amp + " " + key_prsc_y + " not found")

        try:
            self.imsc_area = conversion.str2coordinate(
                self.hdu[headerHDU].header['HIERARCH MAR DET OUT' + amp + " " + 'IMSC'])
        except:
            pass
    # MarManager.DEBUG('Didnt find IMSC for amp ' + str(amp))

# MarManager.DEBUG('Found: Overscan X:' + str(self.areas[0]) + '  Y:' + str(self.areas[1]) + ' -  Prescan X:' + str(self.areas[2]) + '  Y:' + str(self.areas[3]))