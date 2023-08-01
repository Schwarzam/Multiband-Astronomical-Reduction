<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reduction.cosmics`
About ===== cosmics.py is a small and simple python module to detect and clean cosmic ray hits on images (numpy arrays or FITS), using scipy, and based on Pieter van Dokkum's L.A.Cosmic algorithm. L.A.Cosmic = Laplacian cosmic ray detection U{http://www.astro.yale.edu/dokkum/lacosmic/} (article : U{http://arxiv.org/abs/astro-ph/0108003}) Additional features =================== I pimped this a bit to suit my needs : 
        - Automatic recognition of saturated stars, including their full saturation trails.  This avoids that such stars are treated as big cosmics.  Indeed saturated stars tend to get even uglier when you try to clean them. Plus they  keep L.A.Cosmic iterations going on forever.  This feature is mainly for pretty-image production. It is optional, requires one more parameter (a CCD saturation level in ADU), and uses some   nicely robust morphology operations and object extraction.  


        - Scipy image analysis allows to "label" the actual cosmic ray hits (i.e. group the pixels into local islands).  A bit special, but I use this in the scope of visualizing a PSF construction. But otherwise the core is really a 1-to-1 implementation of L.A.Cosmic, and uses the same parameters. Only the conventions on how filters are applied at the image edges might be different. No surprise, this python module is much faster then the IRAF implementation, as it does not read/write every step to disk. Usage ===== Everything is in the file cosmics.py, all you need to do is to import it. You need pyfits, numpy and scipy. See the demo scripts for example usages (the second demo uses f2n.py to make pngs, and thus also needs PIL). Your image should have clean borders, cut away prescan/overscan etc. Todo ==== Ideas for future improvements : 
        - Add something reliable to detect negative glitches (dust on CCD or small traps) 
        - Top level functions to simply run all this on either numpy arrays or directly on FITS files 
        - Reduce memory usage ... easy 
        - Switch from signal to ndimage, homogenize mirror boundaries Malte Tewes, January 2010 

**Global Variables**
---------------
- **laplkernel**
- **growkernel**
- **dilstruct**

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L612"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `fromfits`

```python
fromfits(infilename, hdu=0, verbose=True)
```

Reads a FITS file and returns a 2D numpy array of the data. Use hdu to specify which HDU you want (default = primary = 0) 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L629"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `tofits`

```python
tofits(outfilename, pixelarray, hdr=None, verbose=True)
```

Takes a 2D numpy array and write it into a FITS file. If you specify a header (pyfits format, as returned by fromfits()) it will be used for the image. You can give me boolean numpy arrays, I will convert them into 8 bit integers. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L658"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `subsample`

```python
subsample(a)
```

Returns a 2x2-subsampled version of array a (no interpolation, just cutting pixels in 4). The version below is directly from the scipy cookbook on rebinning : U{http://www.scipy.org/Cookbook/Rebinning} There is ndimage.zoom(cutout.array, 2, order=0, prefilter=False), but it makes funny borders. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L686"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `rebin`

```python
rebin(a, newshape)
```

Auxiliary function to rebin an ndarray a. U{http://www.scipy.org/Cookbook/Rebinning} ``` a=rand(6,4); b=rebin(a,(3,2))```
         



---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L711"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `rebin2x2`

```python
rebin2x2(a)
```

Wrapper around rebin that actually rebins 2 by 2 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `cosmicsimage`




<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    rawarray,
    pssl=0.0,
    gain=2.2,
    readnoise=10.0,
    sigclip=5.0,
    sigfrac=0.3,
    objlim=5.0,
    satlevel=50000.0,
    verbose=True
)
```

sigclip : increase this if you detect cosmics where there are none. Default is 5.0, a good value for earth-bound images. objlim : increase this if normal stars are detected as cosmics. Default is 5.0, a good value for earth-bound images. 

Constructor of the cosmic class, takes a 2D numpy array of your image as main argument. sigclip : laplacian-to-noise limit for cosmic ray detection  objlim : minimum contrast between laplacian image and fine structure image. Use 5.0 if your image is undersampled, HST, ... 

satlevel : if we find agglomerations of pixels above this level, we consider it to be a saturated star and do not try to correct and pixels around it. A negative satlevel skips this feature. 

pssl is the previously subtracted sky level ! 

real   gain    = 1.8          # gain (electrons/ADU)    (0=unknown) real   readn   = 6.5                  # read noise (electrons) (0=unknown) ##gain0  string statsec = "*,*"       # section to use for automatic computation of gain real   skyval  = 0.           # sky level that has been subtracted (ADU) real   sigclip = 3.0          # detection limit for cosmic rays (sigma) real   sigfrac = 0.5          # fractional detection limit for neighbouring pixels real   objlim  = 3.0           # contrast limit between CR and underlying object int    niter   = 1            # maximum number of iterations     




---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clean`

```python
clean(mask=None, verbose=None)
```

Given the mask, we replace the actual problematic pixels with the masked 5x5 median value. This mimics what is done in L.A.Cosmic, but it's a bit harder to do in python, as there is no readymade masked median. So for now we do a loop... Saturated stars, if calculated, are also masked : they are not "cleaned", but their pixels are not used for the interpolation. 

We will directly change self.cleanimage. Instead of using the self.mask, you can supply your own mask as argument. This might be useful to apply this cleaning function iteratively. But for the true L.A.Cosmic, we don't use this, i.e. we use the full mask at each iteration. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L507"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `findholes`

```python
findholes(verbose=True)
```

Detects "negative cosmics" in the cleanarray and adds them to the mask. This is not working yet. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L270"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `findsatstars`

```python
findsatstars(verbose=None)
```

Uses the satlevel to find saturated stars (not cosmics !), and puts the result as a mask in self.satstars. This can then be used to avoid these regions in cosmic detection and cleaning procedures. Slow ... 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L349"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getcleanarray`

```python
getcleanarray()
```

For external use only, as it returns the cleanarray minus pssl ! 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getdilatedmask`

```python
getdilatedmask(size=3)
```

Returns a morphologically dilated copy of the current mask. size = 3 or 5 decides how to dilate. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L340"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getmask`

```python
getmask()
```





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L343"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getrawarray`

```python
getrawarray()
```

For external use only, as it returns the rawarray minus pssl ! 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L327"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getsatstars`

```python
getsatstars(verbose=None)
```

Returns the mask of saturated stars after finding them if not yet done. Intended mainly for external use. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L356"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `guessbackgroundlevel`

```python
guessbackgroundlevel()
```

Estimates the background level. This could be used to fill pixels in large cosmics. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `labelmask`

```python
labelmask(verbose=None)
```

Finds and labels the cosmic "islands" and returns a list of dicts containing their positions. This is made on purpose for visualizations a la f2n.drawstarslist, but could be useful anyway. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L365"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `lacosmiciteration`

```python
lacosmiciteration(verbose=None)
```

Performs one iteration of the L.A.Cosmic algorithm. It operates on self.cleanarray, and afterwards updates self.mask by adding the newly detected cosmics to the existing self.mask. Cleaning is not made automatically ! You have to call clean() after each iteration. This way you can run it several times in a row to to L.A.Cosmic "iterations". See function lacosmic, that mimics the full iterative L.A.Cosmic algorithm. 

Returns a dict containing 
        - niter : the number of cosmic pixels detected in this iteration 
        - nnew : among these, how many were not yet in the mask 
        - itermask : the mask of pixels detected in this iteration 
        - newmask : the pixels detected that were not yet in the mask 

If findsatstars() was called, we exclude these regions from the search. 

---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/reduction/cosmics.py#L564"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(maxiter=4, verbose=False)
```

Full artillery :-) 
        - Find saturated stars 
        - Run maxiter L.A.Cosmic iterations (stops if no more cosmics are found) 

Stops if no cosmics are found or if maxiter is reached. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
