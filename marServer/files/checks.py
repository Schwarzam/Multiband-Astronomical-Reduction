from shutil import copyfile
from django.conf import settings
from files.models import FinalTiles, FieldImages, CurrentConfig, SciByFilter, IndividualFile
import pandas as pd

from astropy.io import fits
from files.auxs import get_master_path, getFilePathRootFits
from files.trilogy import Trilogy

import mar
from mar.config import MarManager
import os

from files.auxs import removeRootFitsPath 

def create_12_band_im(field, overwrite=False):
    im = FieldImages.objects.filter(field=field).first()
    if im is not None and not overwrite:
        #MarManager.INFO(f"Image for {field} already exists. Skipping.")
        return

    res = FinalTiles.objects.filter(field=field).all()

    df = pd.DataFrame(list(res.values()))

    bands = ["G", "R", "I", "Z", "U", "F378", "F395", "F410", "F430", "F515", "F660", "F861"]
    bands.sort()
    
    bs = list(df["band"].unique())
    bs.sort()

    if (bs == bands):
        MarManager.INFO(f"Found all bands for {field} - Creating Trilogy image.")
    else:
        pass

    pathdict = {}

    try:
        for band in bands:
            pathdict[band] = getFilePathRootFits(df[df["band"] == band]["file_path"].values[0])
    except:
        #MarManager.WARN(f"Failed to create Trilogy image for {field}.")
        return

    request_order = 'R,I,F861,Z-G,F515,F660-U,F378,F395,F410,F430'
    
    t = Trilogy(pathdict, request_order)
    
    tilepath = os.path.join(get_master_path("TILES"), field)
    final_path = os.path.join(tilepath, f"{field}.png")
    t.save(final_path)

    db = FieldImages.objects.filter(field=field).first()
    if db is None:
        db = FieldImages(
            field=field,
            file_path=removeRootFitsPath(final_path),
        )
        db.save()

    MarManager.INFO(f"Created Trilogy image for {field}.")

def create_all_12bands():
    all_fields = FinalTiles.objects.values("field").distinct()

    bands = ["G", "R", "I", "Z", "U", "F378", "F395", "F410", "F430", "F515", "F660", "F861"]
    bands.sort()

    for value in all_fields:
        create_12_band_im(value["field"])

def check_crvals():
    inds = IndividualFile.objects.filter(file_type="PROCESSED", status=5).all()

    for file in inds:
        if file.crval1 is None or file.crval2 is None:
            MarManager.WARN(f"CRVAL1 or CRVAL2 is None for {file.file_path}.")
            if '.fz' in file.file_path:
                header = fits.getheader(getFilePathRootFits(file.file_path), ext=1)
            else:
                header = fits.getheader(getFilePathRootFits(file.file_path))
            file.crval1 = header['CRVAL1']
            file.crval2 = header['CRVAL2']
            file.save()
        
        if file.raw_sci.crval1 is None or file.raw_sci.crval2 is None:
            MarManager.WARN(f"CRVAL1 or CRVAL2 is None for {file.raw_sci.file_path}.")
            if '.fz' in file.raw_sci.file_path:
                header = fits.getheader(getFilePathRootFits(file.raw_sci.file_path), ext=1)
            else:
                header = fits.getheader(getFilePathRootFits(file.raw_sci.file_path))
            file.raw_sci.crval1 = header['CRVAL1']
            file.raw_sci.crval2 = header['CRVAL2']
            file.raw_sci.save()

    finals = FinalTiles.objects.all()

    for file in finals:
        if file.crval1 is None or file.crval2 is None:
            MarManager.WARN(f"CRVAL1 or CRVAL2 is None for {file.file_path}.")
            if '.fz' in file.file_path:
                header = fits.getheader(getFilePathRootFits(file.file_path), ext=1)
            else:
                header = fits.getheader(getFilePathRootFits(file.file_path))
            file.crval1 = header['CRVAL1']
            file.crval2 = header['CRVAL2']
            file.save()



def get_current_config():
    MarManager.INFO("Getting current config...")
    default_path = os.path.join(settings.ROOTFITS, "CONFIG", "defaultconfig.yaml")
    if not os.path.exists(default_path):
        copyfile(os.path.join(mar.__path__[0], 'config', 'defaultconfig.yaml'), default_path)
        CurrentConfig(name="defaultconfig.yaml", current=True).save()
        curr_path = default_path
    else:
        curr = CurrentConfig.objects.filter(current=True).first()
        if curr is None:
            MarManager.INFO("No current config found. Switching to default.")
            curr = CurrentConfig.objects.filter(name="defaultconfig.yaml").first()
            if curr is None:
                curr = CurrentConfig(name="defaultconfig.yaml", current=True)
            curr.current = True
            curr.save()
        curr_path = os.path.join(settings.ROOTFITS, "CONFIG", curr.name)

        MarManager.INFO(f"Loaded current config: {curr.name}")

    res = mar.env.load_config(curr_path)
    if res is not None:
        MarManager.INFO(res)
        

def run_checks():

    ## Run any django ORM commands here.
    import sys
    print("Python version")
    print (sys.version)
    print("Version info.")
    print (sys.version_info)

    ##

    MarManager.INFO("Running checks...")
    # This will run synchronously - the server will wait
    try:
        get_current_config()
    except Exception as e:
        MarManager.WARN(f"Failed to load current config: {e}")

    ## This will run asynchonously
    #MarManager.submit(check_crvals)
    MarManager.submit(create_all_12bands)
    
    MarManager.INFO("Checks complete.")
