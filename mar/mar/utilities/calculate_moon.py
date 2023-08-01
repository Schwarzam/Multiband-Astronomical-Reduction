 #!/usr/bin/env python
import sys
import numpy as np
import argparse as ap
from os.path import basename
from astropy.io import fits

__script_name__ = basename(sys.argv[0])
__script_desc__ = 'Reads S-PLUS Image FITS Header and calculates moon '
__script_desc__ += 'position and illumination at the DATETIME of the '
__script_desc__ += 'observation.'

def parse_arguments():
    parser = ap.ArgumentParser(description=__script_desc__)
    parser.add_argument('filename', metavar='FITSFILE', type=str, 
                        help='Observed Image FITS filename')
    parser.add_argument('--append', '-A', action='store_true', default=False, 
                        help='Append new information to the Image FITS header')   
    return parser.parse_args(args=sys.argv[1:])

def print_moon_summary(hdr):
    print(f'OBJECT COORD (RA, DEC) : ({hdr["ra"]}, {hdr["dec"]})')
    print(f'T80S DATETIME OBS: {hdr["DATE-OBS"]}')
    print(f'T80S DATETIME INI OBS: {hdr["OBSINIDT"]}')
    print(f'OBJECT COORD INI OBS (ALT, AZ) : ({hdr["OBSIALTI"]} deg, {hdr["OBSIAZIM"]} deg)')
    print(f'MOON SEPARATION INI OBS: {hdr["MOONISEP"]} deg')
    print(f'MOON ILLUMINATION INI OBS: {hdr["MOONIILL"]}')
    print(f'T80S DATETIME END OBS: {hdr["OBSFINDT"]}')
    print(f'\tOBS DURATION: {hdr["OBSDURAT"]} s')
    print(f'OBJECT COORD END OBS (ALT, AZ) : ({hdr["OBSFALTI"]} deg, {hdr["OBSFAZIM"]} deg)')
    print(f'MOON SEPARATION END OBS: {hdr["MOONFSEP"]} deg')
    print(f'MOON ILLUMINATION END OBS: {hdr["MOONFILL"]}')
    print(f'####################################')
    print(f'MEAN MOON SEPARATION: {hdr["MOONMSEP"]} deg')
    print(f'MEAN MOON ILLUMINATION: {hdr["MOONMILL"]}')
    print('####################################')

def add_moon_summary_header(hdr):
    '''
    Calculates moon separation and illumination at the time and location
    of some observation. 
    
    It Retrieves location and datetime information from `hdr` (the observed
    image HDU header) and writes to the header new cards with the moon 
    information.

    New Cards added to FITS Header `hdr`:

    OBSINIDT : Initial datetime of the observation
    OBSFINDT : Final datetime of the observation
    OBSDURAT : Duration of the observation
    OBSIAZIM : Initial azimuth
    OBSFAZIM : Final azimuth
    OBSIALTI : Initial altitude
    OBSFALTI : Final altitude
    MOONISEP : Initial Moon separation
    MOONFSEP : Final Moon separation
    MOONMSEP : Mean Moon separation
    MOONIILL : Initial Moon illumination
    MOONFILL : Final Moon illumination
    MOONMILL : Mean Moon illumination

    Parameters
    ----------
    hdr : :class:`astropy.io.fits.Header`
        The :class:`astropy.io.fits.Header` instance from the observed Image 
        HDU.
    '''
    import astropy.units as u
    from astropy.time import Time
    from zoneinfo import ZoneInfo
    from datetime import datetime, timedelta
    from astropy.coordinates import AltAz, EarthLocation, SkyCoord

    def get_location_moon_illumination(location_time, return_moon=False):
        from astropy.coordinates import get_body

        sun = get_body('sun', time=location_time)
        moon = get_body('moon', time=location_time)
        elongation = sun.separation(moon)
        moon_phase_angle = np.arctan2(
            sun.distance*np.sin(elongation), 
            moon.distance - sun.distance*np.cos(elongation)
        )
        moon_illumination = (1 + np.cos(moon_phase_angle))/2.0    
        if return_moon:
            return moon_illumination, moon
        return moon_illumination

    # Different formats for strftime and strptime
    date_fmt = '%Y-%m-%d'
    time_fmt = '%H:%M:%S.%f'
    datetime_fmt = '{}T{}'.format(date_fmt, time_fmt)
    datetime_fmt_zoneinfo = '{} %z'.format(datetime_fmt)
    
    # Telescope coordinates from Header
    t80s_coordinates = {
        'HEI': eval(hdr.get('HIERARCH T80S TEL GEOELEV'))*u.m,
        'LAT': eval(hdr.get('HIERARCH T80S TEL GEOLAT'))*u.deg,
        'LON': eval(hdr.get('HIERARCH T80S TEL GEOLON'))*u.deg,
    }    
    # Force timezone information
    t80s_zoneinfo = 'America/Santiago'

    # Telescope Earth Location 
    t80s_EL = EarthLocation(
        lat=t80s_coordinates['LAT'], 
        lon=t80s_coordinates['LON'], 
        height=t80s_coordinates['HEI']
    )

    new_cards = {
        'OBSINIDT' : [None, 'Ini dt of the obs'],
        'OBSFINDT' : [None, 'Fin dt of the obs'],
        'OBSDURAT' : [None, 'Duration of the obs (seconds)'],
        'OBSIAZIM' : [None, 'Ini azimuth (degrees)'],
        'OBSFAZIM' : [None, 'Fin azimuth (degrees)'],
        'OBSIALTI' : [None, 'Ini altitude (degrees)'],
        'OBSFALTI' : [None, 'Fin altitude (degrees)'],
        'MOONISEP' : [None, 'Ini Moon sep (degrees)'],
        'MOONFSEP' : [None, 'Fin Moon sep (degrees)'],
        'MOONMSEP' : [None, 'Mean Moon sep (degrees)'],
        'MOONIILL' : [None, 'Ini Moon illum'],
        'MOONFILL' : [None, 'Fin Moon illum'],
        'MOONMILL' : [None, 'Mean Moon illum'],
    }

    # DATETIME FROM DATE-OBS CARD
    str_dt_obs = hdr.get('DATE-OBS', None)
    # DATETIME DATE-OBS UTC
    dt_obs = datetime.strptime(str_dt_obs + ' +00:00', datetime_fmt_zoneinfo)
    # DATETIME DATE-OBS T80-S
    t80s_dt_obs = dt_obs.astimezone(ZoneInfo(t80s_zoneinfo))
    # INITIAL AND FINAL TIME OF THE OBS
    str_time_obs = hdr.get('TIME', None)
    str_time_obs = str_time_obs.split(' to ')
    str_time_ini_obs, str_time_fin_obs = str_time_obs
    # DATETIME INI OBS T80-S
    str_dt_ini_obs = '{}T{} {}'.format(
        t80s_dt_obs.strftime(datetime_fmt.split('T')[0]), 
        str_time_ini_obs, 
        t80s_dt_obs.strftime('%z')
    )  
    dt_ini_obs = datetime.strptime(str_dt_ini_obs, datetime_fmt_zoneinfo).replace(tzinfo=ZoneInfo(t80s_zoneinfo))
    # INI OBS T80-S astropy.time.Time class
    delta_time = (dt_ini_obs - t80s_dt_obs).total_seconds()
    if (delta_time < 0):
        dt_ini_obs += timedelta(days=1)
        delta_time = (dt_ini_obs - t80s_dt_obs).total_seconds()   
    t80s_T_ini_obs = Time(dt_ini_obs, location=t80s_EL)# - utc_offset_hours
    # DATETIME FIN OBS T80-S
    str_dt_fin_obs = '{}T{} {}'.format(
        t80s_dt_obs.strftime(datetime_fmt.split('T')[0]), 
        str_time_fin_obs, 
        t80s_dt_obs.strftime('%z')
    )
    dt_fin_obs = datetime.strptime(str_dt_fin_obs, datetime_fmt_zoneinfo).replace(tzinfo=ZoneInfo('America/Santiago'))
    # FIN OBS T80-S astropy.time.Time class
    delta_time = (dt_fin_obs - dt_ini_obs).total_seconds()
    if (delta_time < 0):
        dt_fin_obs += timedelta(days=1)
        delta_time = (dt_fin_obs - dt_ini_obs).total_seconds()
        print('delta_time: ', delta_time)
    t80s_T_fin_obs = Time(dt_fin_obs, location=t80s_EL)# - utc_offset_hours
    # CALC OBS DURATION IN SECONDS
    time_ini_obs = datetime.strptime(str_time_ini_obs, time_fmt)
    time_fin_obs = datetime.strptime(str_time_fin_obs, time_fmt)
    obs_duration_seconds = (time_fin_obs - time_ini_obs).total_seconds()
    if obs_duration_seconds < 0:
        time_fin_obs += timedelta(days=1)
        obs_duration_seconds = (time_fin_obs - time_ini_obs).total_seconds()
    try:
        assert(delta_time == obs_duration_seconds)
    except:
        print('{}: Calculated OBS duration problem.'.format(__script_name__))

    new_cards['OBSINIDT'][0] = str(dt_ini_obs)
    new_cards['OBSFINDT'][0] = str(dt_fin_obs)
    new_cards['OBSDURAT'][0] = obs_duration_seconds
        
    # Observation Coordinates transformation and moon calculation with astropy.io.coordinates
    c = SkyCoord(ra=hdr['ra'], dec=hdr['dec'], unit=(u.hourangle, u.deg))
    cT_ini = c.transform_to(AltAz(obstime=t80s_T_ini_obs, location=t80s_EL))
    new_cards['OBSIALTI'][0] = f'{cT_ini.alt.value}'
    new_cards['OBSIAZIM'][0] = f'{cT_ini.az.value}'

    cT_fin = c.transform_to(AltAz(obstime=t80s_T_fin_obs, location=t80s_EL))
    new_cards['OBSFALTI'][0] = f'{cT_fin.alt.value}'
    new_cards['OBSFAZIM'][0] = f'{cT_fin.az.value}'

    moon_t80s_ini_illumination, moon_t80s_ini = get_location_moon_illumination(t80s_T_ini_obs, return_moon=True)
    moon_t80_ini_sep = cT_ini.separation(moon_t80s_ini)
    new_cards['MOONISEP'][0] = f'{moon_t80_ini_sep.value}'
    new_cards['MOONIILL'][0] = f'{moon_t80s_ini_illumination}'

    moon_t80s_fin_illumination, moon_t80s_fin = get_location_moon_illumination(t80s_T_fin_obs, return_moon=True)
    moon_t80s_fin_sep = cT_fin.separation(moon_t80s_fin)
    new_cards['MOONFSEP'][0] = f'{moon_t80s_fin_sep.value}'
    new_cards['MOONFILL'][0] = f'{moon_t80s_fin_illumination}'

    mms = 0.5*(moon_t80s_fin_sep + moon_t80_ini_sep)
    mmi = 0.5*(moon_t80s_fin_illumination + moon_t80s_ini_illumination)
    new_cards['MOONMSEP'][0] = f'{mms.value}'
    new_cards['MOONMILL'][0] = f'{mmi}'

    for k, v in new_cards.items():
        hdr.set(k, value=v[0], comment=v[1])
    return hdr

if __name__ == '__main__':
    # Parse arguments
    args = parse_arguments()

    hdul = fits.open(args.filename, mode='update')

    add_moon_summary_header(hdul[1].header)
    print_moon_summary(hdul[1].header)   

    if args.append:
        print(f'{__script_name__}: {args.filename}: writting moon information to FITS header')
        hdul.writeto(args.filename, overwrite=True, checksum=True)
