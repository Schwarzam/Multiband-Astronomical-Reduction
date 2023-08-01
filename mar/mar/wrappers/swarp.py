import mar
import os

from mar.wrappers.wrappersoperation import *
from mar.wrappers.terminal import runCommand

from mar.config import MarManager

marConf = mar.AttributeDict(mar.env.marConf.Swarp)

class Swarp(readWriteCats):
    """
    A class to run the SWarp software for creating co-added images from multiple input images.

    Args:
        image (str, optional): The name of the input FITS image to be co-added. Default is None.
        addconf (dict, optional): Additional configuration parameters to add to the default configuration. Default is None.
        defaultconf (dict, optional): A dictionary of the entire configuration, to overwrite all of the default configuration.
        read_addconf (str, optional): A path to a file containing a configuration dictionary to add to the default configuration.
        read_defaultconf (str, optional): A path to a file containing a dictionary of the entire configuration, to overwrite all of the default configuration. 
        outdir (str, optional): The output directory for the co-added FITS image. Default is '/tmp/'.
        command (str, optional): The SWarp executable command to use. Default is 'swarp'.

    Attributes:
        command (str): The SWarp executable command to use.
        image (str): The name of the input FITS image to be co-added.
        path (str): The output directory for the co-added FITS image.
        config (dict): A dictionary of the default SWarp configuration parameters and their default values.

    Methods:
        run(self): Runs SWarp on the input FITS image with the current configuration parameters.
    """
    def __init__(self, image=None, addconf=None, defaultconf=None, read_addconf=None, read_defaultconf=None, outdir='/tmp/', command='swarp'):
        """
        Initializes a new instance of the Swarp class with the specified input FITS image, additional configuration parameters,
        default configuration dictionary, configuration file paths, output directory and SWarp executable command.
        """
        readWriteCats.__init__(self)

        self.command = command
        self.image = image
        self.path = outdir

        self.config = {
                'IMAGEOUT_NAME':{'value': os.path.join(self.path, 'coadd.fits'), 'comment':''},
                'WEIGHTOUT_NAME':{'value': os.path.join(self.path, 'coadd.weight.fits'), 'comment':''},
                'HEADER_ONLY':{'value':'N', 'comment':''},
                'HEADER_SUFFIX':{'value':'.head', 'comment':''},
                'WEIGHT_TYPE':{'value':'MAP_WEIGHT', 'comment':''},
                'RESCALE_WEIGHTS':{'value':'Y', 'comment':''},
                'WEIGHT_SUFFIX':{'value':'.swmk.fits', 'comment':''},
                'WEIGHT_THRESH':{'value':'0.00001', 'comment':''},
                'WEIGHT_IMAGE':{'value':'', 'comment':''},
                'COMBINE':{'value':'Y', 'comment':''},
                'COMBINE_TYPE':{'value':'AVERAGE', 'comment':''},
                'BLANK_BADPIXELS':{'value':'N', 'comment':''},
                'CELESTIAL_TYPE':{'value':'NATIVE', 'comment':''},
                'PROJECTION_TYPE':{'value':'TAN', 'comment':''},
                'PROJECTION_ERR':{'value':'0.001', 'comment':''},
                'CENTER_TYPE':{'value':'ALL', 'comment':''},
                'CENTER':{'value':'00:00:00.0, +00:00:00.0', 'comment':''},
                'PIXELSCALE_TYPE':{'value':'MEDIAN', 'comment':''},
                'PIXEL_SCALE':{'value':'0.0', 'comment':''},
                'IMAGE_SIZE':{'value':'0', 'comment':''},
                'RESAMPLE':{'value':'Y', 'comment':''},
                'RESAMPLE_DIR':{'value': os.path.join(self.path, '.'), 'comment':''},
                'RESAMPLE_SUFFIX':{'value':'.resamp.fits', 'comment':''},
                'RESAMPLING_TYPE':{'value':'LANCZOS3', 'comment':''},
                'OVERSAMPLING':{'value':'0', 'comment':''},
                'INTERPOLATE':{'value':'N', 'comment':''},
                'FSCALASTRO_TYPE':{'value':'VARIABLE', 'comment':''},
                'FSCALE_KEYWORD':{'value':'FLXSCALE', 'comment':''},
                'FSCALE_DEFAULT':{'value':'1.0', 'comment':''},
                'GAIN_KEYWORD':{'value':'GAIN', 'comment':''},
                'GAIN_DEFAULT':{'value':'0.0', 'comment':''},
                'SATLEV_KEYWORD':{'value':'SATURATE', 'comment':''},
                'SATLEV_DEFAULT':{'value': 60000.0, 'comment':''},
                'SUBTRACT_BACK':{'value':'Y', 'comment':''},
                'BACK_TYPE':{'value':'AUTO', 'comment':''},
                'BACK_DEFAULT':{'value':'0.0', 'comment':''},
                'BACK_SIZE':{'value':'256', 'comment':''},
                'BACK_FILTERSIZE':{'value':'3', 'comment':''},
                'BACK_FILTTHRESH':{'value':'0.0', 'comment':''},
                'VMEM_DIR':{'value':'/dev/shm/', 'comment':''},
                'VMEM_MAX':{'value':'2048', 'comment':''},
                'MEM_MAX':{'value':'2048', 'comment':''},
                'COMBINE_BUFSIZE':{'value':'1024', 'comment':''},
                'DELETE_TMPFILES':{'value':'N', 'comment':''},
                'COPY_KEYWORDS':{'value':'', 'comment':''},
                'WRITE_FILEINFO':{'value':'N', 'comment':''},
                'WRITE_XML':{'value':'Y', 'comment':''},
                'XML_NAME':{'value': os.path.join(self.path, 'swarp.xml'), 'comment':''},
                'XSL_URL':{'value':'file:///usr/share/swarp/swarp.xsl', 'comment':''},
                'NNODES':{'value':'1', 'comment':''},
                'NODE_INDEX':{'value':'0', 'comment':''},
                'VERBOSE_TYPE':{'value':'NORMAL', 'comment':''},
                'NTHREADS':{'value':f'{marConf.NTHREADS}', 'comment':''},
        }
        
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
        """Runs SWarp on the input FITS image with the current configuration parameters.
        """        
        if self.image is None:
            return ('Image not found')
        
        self.confile = os.path.join(self.path, 'swarp.config')
        self.write_file(self.confile)
        
        MarManager.INFO('Swarp - Running Swarp')
        command = self.command + ' ' + self.image + ' -c ' + self.confile
 
        code = runCommand(command, timeout = marConf.TIMEOUT)
        MarManager.INFO('swarp ran with code ' + str(code))


"""
config = config = {"COPY_KEYWORDS": "EXPTIME,OBJECTDATE-OBS,AIRMASS,PI-COI,TELESCOP,INSTRUME,FILTER,PRJ_ID,PRJ_VER","SUBTRACT_BACK": "Y", "BACK_FILTERSIZE": 5, "BACK_SIZE": 1024, "PIXEL_SCALE": 0.55, "IMAGE_SIZE": 11000, "CENTER_TYPE": "MANUAL", "PIXELSCALE_TYPE": "MANUAL", "WEIGHT_TYPE": "MAP_WEIGHT", "CENTER": "58.22959699954, -58.2576642256", "GAIN_DEFAULT": "0.95", "CELESTIAL_TYPE":"EQUATORIAL", "COMBINE_TYPE": "MEDIAN"}
image = '/home/ubuntu/Home/Documents/testCoadded/CRmask/corr_SPLUS-20210114-022736.fits /home/ubuntu/Home/Documents/testCoadded/CRmask/corr_SPLUS-20210114-022905.fits /home/ubuntu/Home/Documents/testCoadded/CRmask/corr_SPLUS-20210114-023036.fits'
masks = '/home/ubuntu/Home/Documents/testCoadded/CRmask/inverted/maskcorr_SPLUS-20210114-022736.fits /home/ubuntu/Home/Documents/testCoadded/CRmask/inverted/maskcorr_SPLUS-20210114-022905.fits /home/ubuntu/Home/Documents/testCoadded/CRmask/inverted/maskcorr_SPLUS-20210114-023036.fits'
config['WEIGHT_IMAGE'] = masks
s = mar.wrappers.Swarp(image, addconf=config, outdir="/home/ubuntu/Home/Documents/swarp")

s.run()
"""

"""
config = config = {"COPY_KEYWORDS": "OBJECTDATE-OBS,AIRMASS,PI-COI,TELESCOP,INSTRUME,FILTER,PRJ_ID,PRJ_VER", "BACK_FILTERSIZE": 5, "BACK_SIZE": 1024, "PIXEL_SCALE": 0.55, "IMAGE_SIZE": 11000, "CENTER_TYPE": "MANUAL", "PIXELSCALE_TYPE": "MANUAL", "WEIGHT_TYPE": "MAP_WEIGHT", "CENTER": "58.22959699954, -58.2576642256", "GAIN_DEFAULT": "0.95","RESAMPLE": "N" , "CELESTIAL_TYPE":"EQUATORIAL", "COMBINE_TYPE": "WEIGHTED", "SUBTRACT_BACK": "N"}
image = '/home/ubuntu/Home/Documents/testCoadded/swarp/corr_SPLUS-20210114-022736.resamp.fits /home/ubuntu/Home/Documents/testCoadded/swarp/corr_SPLUS-20210114-022905.resamp.fits /home/ubuntu/Home/Documents/testCoadded/swarp/corr_SPLUS-20210114-023036.resamp.fits'
masks = '/home/ubuntu/Home/Documents/testCoadded/swarp/corr_SPLUS-20210114-022736.resamp.weight.fits /home/ubuntu/Home/Documents/testCoadded/swarp/corr_SPLUS-20210114-022905.resamp.weight.fits /home/ubuntu/Home/Documents/testCoadded/swarp/corr_SPLUS-20210114-023036.resamp.weight.fits'
config['WEIGHT_IMAGE'] = masks
s = mar.wrappers.Swarp(image, addconf=config, outdir="/home/ubuntu/Home/Documents/swarp")
s.run()

"""