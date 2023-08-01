import mar
import os

from astropy.io import votable
from astropy.table import Table
from astropy.io import fits

from mar.wrappers.terminal import runCommand
from mar.wrappers.wrappersoperation import *

from mar.config import MarManager


marConf = mar.AttributeDict(mar.env.marConf.PSFex)

class PSFex(readWriteCats):
    """
    A class for running PSFex, which models point spread functions (PSFs) of astronomical images based on selected point sources.

    Args:
        catalog (str): Input catalog to extract PSF model.
        command (str): Command to run PSFex.
        folder (str): Folder to store output files.

    Attributes:
        command (str): Command to run PSFex.
        catalog (str): Input catalog to extract PSF model.
        folder (str): Folder to store output files.
        config (dict): Configuration dictionary.

    Methods:
        run(): Runs PSFex on the catalog to extract PSF model.
        getPSFinfo(): Extracts PSF model parameters from XML output.

    """
    def __init__(self, catalog=None, command = "psfex", folder = "./outputs/"):
        """
        Initialize a PSFex object.

        Args:
            catalog (str): Input catalog to extract PSF model.
            command (str): Command to run PSFex.
            folder (str): Folder to store output files.
        """
        readWriteCats.__init__(self)

        self.command = command
        self.catalog = catalog
        self.folder = folder

        self.config = {
            #PSF model
            'BASIS_TYPE': {'value': marConf.PSFEX_BASIS_TYPE, 'comment': 'NONE, PIXEL, GAUSS-LAGUERRE or FILE'},
            'BASIS_NUMBER': {'value': marConf.PSFEX_BASIS_NUMBER, 'comment': 'Basis number or parameter'},
            'BASIS_NAME': {'value': 'basis.fits', 'comment': 'Basis filename (FITS data-cube)'},
            'BASIS_SCALE': {'value': '1.0', 'comment': 'Gauss-Laguerre beta parameter'},
            'NEWBASIS_TYPE': {'value': 'NONE', 'comment': ' or PCA_COMMON'},
            'NEWBASIS_NUMBER': {'value': '8', 'comment': 'Number of new basis vectors'},
            'PSF_SAMPLING': {'value': marConf.PSFEX_PSF_SAMPLING, 'comment': 'Sampling step in pixel units (0.0 = auto)'},
            'PSF_PIXELSIZE': {'value': '1.0', 'comment': 'Effective pixel size in pixel step units'},
            'PSF_ACCURACY': {'value': '0.01', 'comment': 'Accuracy to expect from PSF "pixel" values'},
            'PSF_SIZE': {'value': marConf.PSFEX_PSF_SIZE, 'comment': 'Image size of the PSF model'},
            'PSF_DGEOCORRECT': {'value': 'N', 'comment': 'Use diff. geom. maps (if provided) Y/N?'},
            'PSF_RECENTER': {'value': 'N', 'comment': 'Allow recentering of PSF-candidates Y/N ?'},
            'MEF_TYPE': {'value': 'INDEPENDENT', 'comment': 'INDEPENDENT or COMMON'},

            #Point source measurements
            'CENTER_KEYS': {'value': 'X_IMAGE,Y_IMAGE', 'comment': 'Catalogue parameters for source pre-centering'},
            'PHOTFLUX_KEY': {'value': 'FLUX_APER(1)', 'comment': 'Catalogue parameter for photometric norm.'},
            'PHOTFLUXERR_KEY': {'value': 'FLUXERR_APER(1)', 'comment': 'Catalogue parameter for photometric error'},
            
            #PSF variability
            'PSFVAR_KEYS': {'value': 'X_IMAGE,Y_IMAGE', 'comment': 'Catalogue or FITS (preceded by :) params'},
            'PSFVAR_GROUPS': {'value': '1,1', 'comment': 'Group tag for each context key'},
            'PSFVAR_DEGREES': {'value': marConf.PSFEX_PSFVAR_DEGREES, 'comment': 'Polynom degree for each group'},
            'PSFVAR_NSNAP': {'value': marConf.PSFEX_PSFVAR_NSNAP, 'comment': 'Number of PSF snapshots per axis'},
            'HIDDENMEF_TYPE': {'value': 'COMMON', 'comment': 'INDEPENDENT or COMMON'},
            'STABILITY_TYPE': {'value': 'EXPOSURE', 'comment': 'EXPOSURE or SEQUENCE'},
            
            #Sample selection
            'SAMPLE_AUTOSELECT': {'value': 'Y', 'comment': 'Automatically select the FWHM (Y/N) ?'},
            'SAMPLEVAR_TYPE': {'value': 'SEEING', 'comment': 'File-to-file PSF variability: NONE or SEEING'},
            'SAMPLE_FWHMRANGE': {'value': '2.0,10.0', 'comment': 'Allowed FWHM range'},
            'SAMPLE_VARIABILITY': {'value': '0.2', 'comment': 'Allowed FWHM variability (1.0 = 100%)'},
            'SAMPLE_MINSN': {'value': '20', 'comment': 'Minimum S/N for a source to be used'},
            'SAMPLE_MAXELLIP': {'value': '0.3', 'comment': 'Maximum (A-B)/(A+B) for a source to be used'},
            'SAMPLE_FLAGMASK': {'value': '0x00fe', 'comment': 'Rejection mask on SExtractor FLAGS'},
            'SAMPLE_WFLAGMASK': {'value': '0x0000', 'comment': 'Rejection mask on SExtractor FLAGS_WEIGHT'},
            'SAMPLE_IMAFLAGMASK': {'value': '0x0', 'comment': 'Rejection mask on SExtractor IMAFLAGS_ISO'},
            'BADPIXEL_FILTER': {'value': 'N', 'comment': 'Filter bad-pixels in samples (Y/N) ?'},
            'BADPIXEL_NMAX': {'value': '0', 'comment': 'Maximum number of bad pixels allowed'},
            
            #PSF homogeneisation kernel
            'HOMOBASIS_TYPE': {'value': 'NONE', 'comment': 'NONE or GAUSS-LAGUERRE'},
            'HOMOBASIS_NUMBER': {'value': '10', 'comment': 'Kernel basis number or parameter'},
            'HOMOBASIS_SCALE': {'value': '1.0', 'comment': 'GAUSS-LAGUERRE beta parameter'},
            'HOMOPSF_PARAMS': {'value': tuple(marConf.PSFEX_HOMOPSF_PARAMS), 'comment': 'Moffat parameters of the idealised PSF'},
            'HOMOKERNEL_DIR': {'value': '', 'comment': 'Where to write kernels (empty=same as input)'},
            'HOMOKERNEL_SUFFIX': {'value': '.homo.fits', 'comment': 'Filename extension for homogenisation kernels'},
            
            #Output catalogs
            'OUTCAT_TYPE': {'value': 'NONE', 'comment': 'NONE, ASCII_HEAD, ASCII, FITS_LDAC'},
            'OUTCAT_NAME': {'value': 'psfex_out.cat', 'comment': 'Output catalog filename'},
            
            #Check-plots
            'CHECKPLOT_DEV': {'value': 'PNG', 'comment': ' JPEG, AQT, PDF or SVG'},
            'CHECKPLOT_RES': {'value': '0', 'comment': 'Check-plot resolution (0 = default)'},
            'CHECKPLOT_ANTIALIAS': {'value': 'Y', 'comment': 'Anti-aliasing using convert (Y/N) ?'},
            'CHECKPLOT_TYPE': {'value': 'NONE', 'comment': 'SELECTION_FWHM,FWHM,ELLIPTICITY,COUNTS,COUNT_FRACTION,CHI2, RESIDUALS or NONE'},
            'CHECKPLOT_NAME': {'value': 'selfwhm,fwhm,ellipticity,counts,countfrac,chi2,resi', 'comment': ''},
            
            #Check-Images
            'CHECKIMAGE_TYPE': {'value': 'NONE', 'comment': 'CHI,PROTOTYPES,SAMPLES,RESIDUALS,SNAPSHOTS or MOFFAT,-MOFFAT,-SYMMETRICAL'},
            'CHECKIMAGE_NAME': {'value': 'chi.fits,proto.fits,samp.fits,resi.fits,snap.fits', 'comment': ' Check-image filenames'},
            'CHECKIMAGE_CUBE': {'value': 'N', 'comment': 'Save check-images as datacubes (Y/N) ?'},
            'PSF_DIR': {'value': os.path.join(folder, ''), 'comment': 'Where to write PSFs (empty=same as input)'},
            'PSF_SUFFIX': {'value': '.psf', 'comment': 'Filename extension for output PSF filename'},
            'VERBOSE_TYPE': {'value': 'NORMAL', 'comment': 'can be QUIET,NORMAL,LOG or FULL'},
            'WRITE_XML': {'value': 'Y', 'comment': 'Write XML file (Y/N)?'},
            'XML_NAME': {'value': os.path.join(folder, 'psfex.xml'), 'comment': 'Filename for XML output'},
            'XSL_URL': {'value': 'file:///usr/local/share/psfex/psfex.xsl', 'comment': ' Filename for XSL style-sheet'},
            'NTHREADS': {'value': marConf.NTHREADS, 'comment': ' 0 = automatic'}

        }

    def run(self):
        """
        Runs PSFex with the configured options.
        """
        self.confile = os.path.join(self.folder, 'config.psfex')
        self.write_file(self.confile, mode="scamp")

        MarManager.INFO('Running - PSFex')

        command = self.command + " " + self.catalog + " -c " + self.confile

        code = runCommand(command, timeout = marConf.TIMEOUT)
        
        MarManager.INFO('sextractor ran with code ' + str(code))

    def getPSFinfo(self):
        """
        Parses the XML output of PSFex and returns a dictionary of relevant
        information.
        """
        v = votable.parse(os.path.join(self.folder, 'psfex.xml'))
        table = v.get_table_by_id('PSF_Fields')

        data = table.array

        keys = ["NStars_Loaded_Total",
                "NStars_Accepted_Total",
                "FWHM_Mean",  # pixel unit
                "FWHM_Min",  # pixel
                "FWHM_Max",  # pixel 
                "Chi2_Mean",
                "MoffatBeta_Mean",
                "Asymmetry_Mean",
                "Ellipticity_Mean"]

        # return {key: data[key].data[0] for key in keys}
        info = {}
        
        try:
            for key in keys:
                info[key] = data[key].data[0]
        except:
            return None
        
        return info



def createVignetCatalog(image, output):
    """
    Creates a catalog of vignettes (small cutouts) of stars in the given image using sextractor.

    :param image: path to the input image file
    :type image: str
    :param output: path to the output catalog file
    :type output: str
    """
    conf = {
        "CATALOG_NAME": output,

        "WEIGHT_TYPE": "NONE",

        "BACK_FILTERSIZE": marConf.VIGNET_BACK_FILTERSIZE,
        "BACK_SIZE": marConf.VIGNET_BACK_SIZE,
        "DETECT_THRESH": marConf.VIGNET_DETECT_THRESH,
        "ANALYSIS_THRESH": marConf.VIGNET_ANALYSIS_THRESH,
        "DETECT_MINAREA": marConf.VIGNET_DETECT_MINAREA,

        "CATALOG_TYPE": 'FITS_LDAC',
        "PHOT_AUTOPARAMS": '2.5,3.5',
        "CHECKIMAGE_TYPE": "NONE",
        "PHOT_FLUXFRAC": marConf.VIGNET_PHOT_FLUXFRAC,

        "FILTER_NAME": os.path.join(mar.__path__[0], 'config/sextractor/gauss_3.0_5x5.conv'), 
        "FILTER": "Y",
        "PHOT_APERTURES": ("%.2f, %.2f, %.2f, %.2f, %.2f, %.2f" % tuple(marConf.VIGNET_PHOT_APERTURES))
    }

    numapers = len(marConf.VIGNET_PHOT_APERTURES)
    vignetsize = [51, 51]

    params = [
                "NUMBER",
                "ALPHA_J2000",
                "DELTA_J2000",
                "VIGNET({0},{1})".format(vignetsize[0], vignetsize[1]),
                "X_IMAGE", "Y_IMAGE",
                "FLUX_AUTO", "FLUXERR_AUTO",
                "MAG_AUTO", "MAGERR_AUTO",
                "FLUX_APER({0})".format(numapers),
                "FLUXERR_APER({0})".format(numapers),
                "MAG_APER({0})".format(numapers),
                "MAGERR_APER({0})".format(numapers),
                "FWHM_IMAGE", "ISOAREA_IMAGE",
                "FLUX_RADIUS", "FLUX_MAX",
                "ELLIPTICITY", "ELONGATION",
                "SNR_WIN",
                "FLAGS",
                "FLAGS_WEIGHT",
                "CLASS_STAR",
                "XWIN_IMAGE", "YWIN_IMAGE"
    ]

    from mar.wrappers.sextractor import SExtr

    inst = SExtr(image=image, folder=os.path.dirname(output), addconf=conf)
    inst.params = params
    inst.run()


    filterCatalogToPSFex(output)


def filterCatalogToPSFex(tablepath):
    """
    Filters the given sextractor catalog file to keep only objects that are
    likely to be good PSF candidates.

    :param tablepath: path to the input catalog file
    :type tablepath: str
    """
    t = Table.read(tablepath, hdu=2)
    f = fits.open(tablepath, mode='update')
    
    selection = (
				(t["FLAGS"] == 0) &
				(t["MAGERR_AUTO"] < marConf.PSFEX_CAT_MAX_MAGERR_AUTO) &
				(t["ELLIPTICITY"] < marConf.PSFEX_CAT_MAX_ELLIPTICITY) &
				(t["ISOAREA_IMAGE"] > marConf.PSFEX_CAT_MIN_ISOAREA_IMAGE) &
				(t["SNR_WIN"] < marConf.PSFEX_CAT_MAX_SNR_WIN)
			)
    
    f[2].data = t[selection].as_array()
    f.flush()
