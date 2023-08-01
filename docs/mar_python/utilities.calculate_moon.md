<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/calculate_moon.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utilities.calculate_moon`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/calculate_moon.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `parse_arguments`

```python
parse_arguments()
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/calculate_moon.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_moon_summary`

```python
print_moon_summary(hdr)
```






---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/utilities/calculate_moon.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `add_moon_summary_header`

```python
add_moon_summary_header(hdr)
```

Calculates moon separation and illumination at the time and location of some observation.  

It Retrieves location and datetime information from `hdr` (the observed image HDU header) and writes to the header new cards with the moon  information. 

New Cards added to FITS Header `hdr`: 

OBSINIDT : Initial datetime of the observation OBSFINDT : Final datetime of the observation OBSDURAT : Duration of the observation OBSIAZIM : Initial azimuth OBSFAZIM : Final azimuth OBSIALTI : Initial altitude OBSFALTI : Final altitude MOONISEP : Initial Moon separation MOONFSEP : Final Moon separation MOONMSEP : Mean Moon separation MOONIILL : Initial Moon illumination MOONFILL : Final Moon illumination MOONMILL : Mean Moon illumination 

Parameters 
---------- hdr : :class:`astropy.io.fits.Header`  The :class:`astropy.io.fits.Header` instance from the observed Image   HDU. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
