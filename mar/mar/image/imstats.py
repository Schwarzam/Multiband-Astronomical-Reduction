import mar 
from astropy.io import fits 
import numpy as np
import random
from astropy.stats import sigma_clip

from mar.config import MarManager

class ComputeStats:
    def __init__(self, marfits=None, headerHDU=0, dataHDU=0, data=None, section=[], steps=11):
        self.hdu = marfits
        self.headerHDU = headerHDU
        self.areas = {}
        self.steps = steps

        self.dataMode = False
        if data is not None:
            self.data = data
            self.dataMode = True
            self.areas[0] = section
        else:
            self.data = marfits[dataHDU].data

            ampSize = mar.utilities.conversion.str2coordinate(marfits[headerHDU].header['HIERARCH MAR DET OUT1 IMSC'])
            self.amps = int(marfits[headerHDU].header['HIERARCH MAR DET OUTPUTS'])

            self.ampSize = (ampSize[1] - ampSize[0], ampSize[3] - ampSize[2])
            self.orders = np.array(mar.env.marConf.Scan['CCD_ORDER'])
            self.indices = np.indices(self.orders.shape)

        self.shape = None

        
        self.values = {'x': [], 'y': [], 'mean': [], 'midpt': [], 'std': []}
        self.stats = {"amedian": None, "amean": None, "astd": None}

        if data is None:
            self.calculateAmps()

        self.allstats = {}
        
    def calcallstats(self):
        MarManager.INFO("Calculating stats.")

        if self.dataMode:
            self.getStats(0)
        else:
            for i in range(1, self.amps+1):
                self.getStats(i)
            
        self.modeavg = np.array([self.allstats[e]['mode']for e in self.allstats.keys()]).mean()
        self.medianavg = np.array([self.allstats[e]['midpt'] for e in self.allstats.keys()]).mean()
        
        auxar = np.array([self.allstats[e]['stdmidpt']for e in self.allstats.keys()])
        self.medianrms = np.sqrt((auxar * auxar).sum() / float(len(auxar)))
        
        self.noiseavg = np.array([self.allstats[e]['noise'] for e in self.allstats.keys()]).mean()
        
        auxar = np.array([self.allstats[e]['stdnoise'] for e in self.allstats.keys()])
        self.noiserms = np.sqrt((auxar * auxar).sum() / float(len(auxar)))
        
    def calculateAmps(self):
        ampSize = self.ampSize
        for i in range(1, self.amps+1):
            y = self.indices[0][(self.orders == i)][0]
            x = self.indices[1][(self.orders == i)][0]

            image_section = [y * ampSize[0], (y + 1) * ampSize[0], x * ampSize[1], (x + 1) * ampSize[1]]
            self.areas[i] = image_section
            
    def getStats(self, amp, lsigma=3, usigma=3, maxiters=2, boxx=20):    
        self.values = {'x': [], 'y': [], 'mean': [], 'midpt': [], 'std': []}
        self.stats = {"amedian": None, "amean": None, "astd": None}
        
        _boxx = int(boxx) / 2
        _boxx_l = _boxx
        if boxx % 2 == 1:
            _boxx_u = _boxx + 1
        else:
            _boxx_u = _boxx

        section = self.areas[amp]

        stepx = float((section[3] - section[2])) / (self.steps)
        stepy = float((section[1] - section[0])) / (self.steps)
        yarr = np.arange(1, section[1] - section[0], stepy) + 0.5 * stepy
        xarr = np.arange(1, section[3] - section[2], stepx) + 0.5 * stepx

        xarr, yarr = np.meshgrid(xarr, yarr)
        xarr = xarr.ravel()
        yarr = yarr.ravel()

        for x, y in zip(xarr, yarr):
            sigdata, lower, upper = sigma_clip(self.data[int(section[0] + y - _boxx_l):
                                          int(section[0] + y + _boxx_u),
                                          int(section[2] + x - _boxx_l):
                                          int(section[2] + x + _boxx_u)],
                                    sigma_lower=lsigma, sigma_upper=usigma, maxiters=maxiters, 
                                    masked=False, axis=None, return_bounds=True)
            
            self.values['x'].append(x)
            self.values['y'].append(y)
            self.values['mean'].append(sigdata.mean(dtype=np.float64))
            self.values['midpt'].append(np.median(sigdata))
            self.values['std'].append(sigdata.std())
            
        self.compute(amp)
        
    def compute(self, amp):
        keys2 = ['amedian', 'amean', 'astd']
        keys = ['midpt', 'mean', 'std']
        
        for k, k2 in zip(keys, keys2):
            self.stats[k2] = {'median': None, 'std': None} 
            self.stats[k2]['median'] = mar.utilities.median_robust(self.values[k], sigma=2, maxiters=1)
            self.stats[k2]['std'] =  mar.utilities.std_robust(self.values[k], n_sigma=2, n=1)
        
        
        self.allstats.setdefault(amp, {'midpt': self.stats['amedian']['median'],
                                       'mode': self.stats['amean']['median'],
                                       'stdmidpt': self.stats['amedian']['std'],
                                       'stdmode': self.stats['amean']['std'],
                                       'noise': self.stats['astd']['median'],
                                       'stdnoise': self.stats['astd']['std']})
        
    def updateHeader(self, generalOnly=False):
        MarManager.INFO("Updating header with stats.")
        h = self.headerHDU
        
        self.hdu[h].header.set('HIERARCH MAR QC NCMODE', round(self.modeavg, 4), 'Mode cor image (ADU)')
        self.hdu[h].header.set('HIERARCH MAR QC NCMIDPT', round(self.medianavg, 4),'Level estim cor (ADU)')
        self.hdu[h].header.set('HIERARCH MAR QC NCNOISE', round(self.noiseavg, 4),'Noise estim cor (ADU)')
        self.hdu[h].header.set('HIERARCH MAR QC NCMIDRMS', round(self.medianrms, 4),'rms level estim cor (ADU)')
        self.hdu[h].header.set('HIERARCH MAR QC NCNOIRMS', round(self.noiserms, 4), 'rms noise estim cor (ADU)')
        
        if generalOnly:
            return
        for amp in range(1, self.amps+1):
            self.hdu[h].header.set(f"HIERARCH MAR PRO OUT{amp} IMSC", 
                             mar.utilities.coordinate2str(self.areas[amp]), f'Mode amp {amp} cor (ADU)')

            self.hdu[h].header.set(f"HIERARCH MAR QC OUT{amp} NCMODE", 
                             round(self.allstats[amp]['mode'], 4), f'Mode amp {amp} cor (ADU)')
            
            self.hdu[h].header.set(f"HIERARCH MAR QC OUT{amp} NCMIDPT", 
                             round(self.allstats[amp]['midpt'], 4), f'Level amp estim {amp} cor (ADU)')
            
            self.hdu[h].header.set(f"HIERARCH MAR QC OUT{amp} NCMIDRMS", 
                             round(self.allstats[amp]['stdmidpt'], 4), f'rms level amp estim {amp} cor (ADU)')
            
            self.hdu[h].header.set(f"HIERARCH MAR QC OUT{amp} NCNOISE", 
                             round(self.allstats[amp]['noise'], 4), f'Noise amp estim {amp} cor (ADU)')
            
            self.hdu[h].header.set(f"HIERARCH MAR QC OUT{amp} NCNOIRMS", 
                             round(self.allstats[amp]['mode'], 4), f'rms noise amp estim {amp} cor (ADU)')
            


'''
hdu = fits.open(path)
x  = mar.image.ComputeStats(hdu)
x.calcallstats()
x.updateHeader()
'''