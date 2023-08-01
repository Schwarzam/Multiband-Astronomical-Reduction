"""
https://www.stsci.edu/~dcoe/trilogy/Intro.html

Trilogy is very easy to use and automatically scales the image data to reveal faint features without saturating bright features.
As used by CLASH and the DECam Legacy Survey.

Reference Coe et al. 2012.
Translated to python3 by github.com/schwarzam.
"""


import astropy.io.fits
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import golden
from PIL import Image
from os import listdir
from os.path import isfile, join

rw, gw, bw = 0.299,  0.587,  0.114  # NTSC (also used by PIL in "convert")
rw, gw, bw = 0.3086, 0.6094, 0.0820  # linear
rw, gw, bw = 0.212671, 0.715160, 0.072169  # D65: red boosted, blue muted a bit, I like it

def get_levels(stampsRGB):
    datasorted = np.sort(stampsRGB.flat)
    datasorted[np.isnan(datasorted)] = 0

    noisesig = 1

    rem, m, r = meanstd(datasorted)
    x0 = 0

    x1 = m + noisesig * r

    x2 = setLevel(datasorted, unsatpercent)

    levels = x0, x1, x2

    return levels

def get_clip(m, m_min=None, m_max=None):
    if m_min == None:
        m_min = min(m)
    if m_max == None:
        m_max = max(m)

    return np.clip(m, m_min, m_max)

def setLevel(data, pp):
    vs = data
    vs = get_clip(vs, 0, None)

    ii = np.array(pp) * len(vs)
    ii = ii.astype('int')
    ii = np.clip(ii, 0, len(vs) - 1)
    levels = vs.take(ii)
    return levels

def rms(x):
    return np.sqrt(np.mean(x ** 2))

def meanstd(datasorted, n_sigma = 3, n = 5):
    x = datasorted

    ihi = nx = len(x)
    ilo = 0

    xsort = x

    for i in range(n):
        xs = xsort[ilo: ihi]

        imed = (ilo+ihi) / 2

        aver = xs[int(imed)]

        std1 = np.std(xs)
        std1 = rms(xs - aver)

        lo = aver - n_sigma * std1
        hi = aver + n_sigma * std1

        ilo = np.searchsorted(xsort, lo)
        ihi = np.searchsorted(xsort, hi, side='right')

        nnx = ihi - ilo

        if nnx == nx:
            break
        else:
            nx = nnx

    remaining = xrem = xs[ilo:ihi]
    mean = np.mean(xrem)
    std = rms(xrem - mean)

    return remaining, mean, std

def RGB2im(RGB):
    data = RGB
    data = np.transpose(data, (1,2,0))  # (3, ny, nx) -> (ny, nx, 3)
    data = np.clip(data, 0, 255)
    data = data.astype('uint8')
    three = data.shape[-1]  # 3 if RGB, 1 if L
    if three == 3:
        im = Image.fromarray(data)
    elif three == 1:
        im = Image.fromarray(data[:,:,0], 'L')
    else:
        print('Data shape not understood: expect last number to be 3 for RGB, 1 for L', data.shape)
        raise Exception  # Raise generic exception and exit

    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    return im

def da(k):
    a1 = k * (x1 - x0) + 1
    a2 = k * (x2 - x0) + 1
    a1n = a1 ** n
    a1n = np.abs(a1n)

    da1 = a1n - a2
    k = np.abs(k)

    if k == 0:
        return da(1e-10)
    else:
        da1 = da1 / k

    return np.abs(da1)

def imscale(data, levels, y1):
    global n, x0, x1, x2
    x0, x1, x2 = levels
    if y1 == 0.5:
        k = (x2 - 2 * x1 + x0) / float(x1 - x0) ** 2
    else:
        n = 1 / y1
        k = abs(golden(da))

    r1 = np.log10(k* (x2-x0) + 1)

    v = np.ravel(data)
    v = get_clip(v, 0, None)

    d = k * (v - x0) + 1
    d = get_clip(d, 1e-30, None)

    z = np.log10(d) / r1
    z = np.clip(z, 0, 1)
    z.shape = data.shape

    z = z * 255
    z = z.astype('uint8')

    return z

def satK2m(K):
    m00 = rw * (1-K) + K
    m01 = gw * (1-K)
    m02 = bw * (1-K)

    m10 = rw * (1-K)
    m11 = gw * (1-K) + K
    m12 = bw * (1-K)

    m20 = rw * (1-K)
    m21 = gw * (1-K)
    m22 = bw * (1-K) + K

    m = np.array([[m00, m01, m02], [m10, m11, m12], [m20, m21, m22]])
    return m

def adjust_saturation(RGB, K):
    m = satK2m(K)
    three, nx, ny = RGB.shape

    RGB.shape = three, nx*ny

    RGB = np.dot(m, RGB)
    RGB.shape = three, nx, ny
    return RGB

class Trilogy():
    def __init__(self, pathdict, reqOrder, dx = None, dy = None, noiselum = 0.15, satpercent = 0.15, colorsatfac = 2):
        sgn = 1

        satpercent = float(satpercent)
        noiselum = float(satpercent)

        global unsatpercent
        unsatpercent = 1 - 0.01 * satpercent

        self.noiselums = {'R': noiselum, 'G': noiselum, 'B': noiselum}

        try:
            self.hduF378 = astropy.io.fits.getdata(pathdict['F378'])
        except:
            pass 
        try:
            self.hduF395 = astropy.io.fits.getdata(pathdict['F395'])
        except:
            pass 
        try:
            self.hduF410 = astropy.io.fits.getdata(pathdict['F410'])
        except:
            pass 
        try:
            self.hduF430 = astropy.io.fits.getdata(pathdict['F430'])
        except:
            pass 
        try:
            self.hduF515 = astropy.io.fits.getdata(pathdict['F515'])
        except:
            pass 
        try:
            self.hduF660 = astropy.io.fits.getdata(pathdict['F660'])
        except:
            pass 
        try:
            self.hduF861 = astropy.io.fits.getdata(pathdict['F861'])
        except:
            pass 
        try:
            self.hduR = astropy.io.fits.getdata(pathdict['R'])
        except:
            pass 
        try:
            self.hduG = astropy.io.fits.getdata(pathdict['G'])
        except:
            pass 
        try:
            self.hduI = astropy.io.fits.getdata(pathdict['I'])
        except:
            pass 
        try:
            self.hduU = astropy.io.fits.getdata(pathdict['U'])
        except:
            pass 
        try:
            self.hduZ = astropy.io.fits.getdata(pathdict['Z'])
        except:
            pass 


        ##tamanho desejado no final
        if not dx:
            try: self.dx = self.hduR.shape[0]
            except: pass
            try: self.dx = self.hduG.shape[0]
            except: pass
            try: self.dx = self.hduZ.shape[0]
            except: pass
            try: self.dx = self.hduU.shape[0]
            except: pass
            try: self.dx = self.hduI.shape[0]
            except: pass
            try: self.dx = self.hduF861.shape[0]
            except: pass
            try: self.dx = self.hduF660.shape[0]
            except: pass
            try: self.dx = self.hduF515.shape[0]
            except: pass
            try: self.dx = self.hduF430.shape[0]
            except: pass
            try: self.dx = self.hduF395.shape[0]
            except: pass
            try: self.dx = self.hduF378.shape[0]
            except: pass
        else:
            self.dx = dx

        if not dy:
            try: self.dy = self.hduR.shape[1]
            except: pass
            try: self.dy = self.hduG.shape[1]
            except: pass
            try: self.dy = self.hduZ.shape[1]
            except: pass
            try: self.dy = self.hduU.shape[1]
            except: pass
            try: self.dy = self.hduI.shape[1]
            except: pass
            try: self.dy = self.hduF861.shape[1]
            except: pass
            try: self.dy = self.hduF660.shape[1]
            except: pass
            try: self.dy = self.hduF515.shape[1]
            except: pass
            try: self.dy = self.hduF430.shape[1]
            except: pass
            try: self.dy = self.hduF395.shape[1]
            except: pass
            try: self.dy = self.hduF378.shape[1]
            except: pass
        else:
            self.dy = dy

        self.ny, self.nx = self.hduR.shape
        self.yc = self.ny / 2
        self.xc = self.nx / 2

        self.ylo = np.clip(self.yc - self.dy/2 + 0, 0, self.ny)
        self.yhi = np.clip(self.yc + self.dy/2 + 0, 0, self.ny)
        self.xlo = np.clip(self.xc - self.dx/2 + 0, 0, self.ny)
        self.xhi = np.clip(self.xc + self.dx/2 + 0, 0, self.ny)

        self.dx = self.yhi - self.ylo
        self.dy = self.xhi - self.xlo

        self.stampsRGB = np.zeros((3, int(self.dy), int(self.dx)))

        R = []
        G = []
        B = []
        for key, value in enumerate(reqOrder.split("-")):
            if key == 0: 
                R = value.split(',')
            if key == 1: 
                G = value.split(',')
            if key == 2: 
                B = value.split(',')



        self.bands = R + G + B
        self.R = R
        self.G = G
        self.B = B

        self.unsatpercent = 1 - 0.01 * satpercent

        self.sgn = 1
        for band in self.bands:
            if band in self.R:
                exec(f"self.data = self.hdu{band}")
                data = self.data[int(self.ylo):int(self.yhi), int(self.xlo):int(self.xhi)]
                self.stampsRGB[0] = self.stampsRGB[0] + sgn * data
            if band in self.G:
                exec(f"self.data = self.hdu{band}")
                data = self.data[int(self.ylo):int(self.yhi), int(self.xlo):int(self.xhi)]
                self.stampsRGB[1] = self.stampsRGB[1] + sgn * data
            if band in self.B:
                exec(f"self.data = self.hdu{band}")
                data = self.data[int(self.ylo):int(self.yhi), int(self.xlo):int(self.xhi)]
                self.stampsRGB[2] = self.stampsRGB[2] + sgn * data

        self.leveldict = {}
        for key, band in enumerate('RGB'):
            level = get_levels(self.stampsRGB[key])
            self.leveldict[f'{band}'] = level

        three, nx, ny = self.stampsRGB.shape
        self.scaled = np.zeros(self.stampsRGB.shape, float)

        RGB = 'RGB'
        for i in range(len(RGB)):
            self.channel = RGB[i]
            self.levels = self.leveldict[RGB[i]]
            self.noiselum = self.noiselums[RGB[i]]
            self.scaled[i] = imscale(self.stampsRGB[i], self.levels, self.noiselum)

        self.scaled = adjust_saturation(self.scaled, colorsatfac)
        self.im = RGB2im(self.scaled)

    def save(self, path):
        plt.imsave(arr = np.array(self.im), fname = path)
        return True

    def get_array(self):
        return np.array(self.im)

class Trilogy_data():
    def __init__(self, F378, F395, F410, F430, F515, F660, F861, R, G, I, U, Z, dx, dy, noiselum, satpercent, colorsatfac):
        self.dx = dx  ##tamanho desejado no final
        self.dy = dy
        sgn = 1

        global unsatpercent
        unsatpercent = 1 - 0.01 * satpercent

        self.noiselums = {'R': noiselum, 'G': noiselum, 'B': noiselum}

        self.hduF378 = F378
        self.hduF395 = F395
        self.hduF410 = F410
        self.hduF430 = F430
        self.hduF515 = F515
        self.hduF660 = F660
        self.hduF861 = F861
        self.hduR = R
        self.hduG = G
        self.hduI = I
        self.hduU = U
        self.hduZ = Z

        self.ny, self.nx = self.hduR.shape
        self.yc = self.ny / 2
        self.xc = self.nx / 2

        self.ylo = np.clip(self.yc - self.dy/2 + 0, 0, self.ny)
        self.yhi = np.clip(self.yc + self.dy/2 + 0, 0, self.ny)
        self.xlo = np.clip(self.xc - self.dx/2 + 0, 0, self.ny)
        self.xhi = np.clip(self.xc + self.dx/2 + 0, 0, self.ny)

        self.dx = self.yhi - self.ylo
        self.dy = self.xhi - self.xlo

        self.stampsRGB = np.zeros((3, int(self.dy), int(self.dx)))

        self.bands = ["R", "G", "I", "U", "B", "F378", "F395", "F410", "F430", "F515", "F660", "F861"]
        self.R = ["R", "I", "F861", "Z"]
        self.G = ["G", "F515", "F660"]
        self.B = ["U", "F378", "F395", "F410", "F430"]

        self.unsatpercent = 1 - 0.01 * satpercent

        self.sgn = 1
        for band in self.bands:
            if band in self.R:
                exec(f"self.data = self.hdu{band}")
                data = self.data[int(self.ylo):int(self.yhi), int(self.xlo):int(self.xhi)]
                self.stampsRGB[0] = self.stampsRGB[0] + sgn * data
            if band in self.G:
                exec(f"self.data = self.hdu{band}")
                data = self.data[int(self.ylo):int(self.yhi), int(self.xlo):int(self.xhi)]
                self.stampsRGB[1] = self.stampsRGB[1] + sgn * data
            if band in self.B:
                exec(f"self.data = self.hdu{band}")
                data = self.data[int(self.ylo):int(self.yhi), int(self.xlo):int(self.xhi)]
                self.stampsRGB[2] = self.stampsRGB[2] + sgn * data

        self.leveldict = {}
        for key, band in enumerate('RGB'):
            level = get_levels(self.stampsRGB[key])
            self.leveldict[f'{band}'] = level

        three, nx, ny = self.stampsRGB.shape
        self.scaled = np.zeros(self.stampsRGB.shape, float)

        RGB = 'RGB'
        for i in range(len(RGB)):
            self.channel = RGB[i]
            self.levels = self.leveldict[RGB[i]]
            self.noiselum = self.noiselums[RGB[i]]
            self.scaled[i] = imscale(self.stampsRGB[i], self.levels, self.noiselum)

        self.scaled = adjust_saturation(self.scaled, colorsatfac)
        self.im = RGB2im(self.scaled)

    def get(self):
        return self.im

    def get_array(self):
        return np.array(self.im)

if __name__ == '__main__':
    import os
    mypath = os.path.dirname(os.path.abspath(__file__))
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    bands = ["R", "G", "I", "U", "Z", "F378", "F395", "F410", "F430", "F515", "F660", "F861"]
    pathdict = {}

    for band in bands:
        for file in onlyfiles:
            if f"_{band}" in file:
                 pathdict[band] = f'{mypath}/{file}'
                 filename = file.replace(f'_{band}', '')
                 filename = filename.replace(f'.fits', '.png')
                 filename = f'{mypath}/{filename}'

    Trilogy(pathdict, noiselum = 0.01).get(path = filename)