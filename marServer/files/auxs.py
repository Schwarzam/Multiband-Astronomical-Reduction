import shutil
from django.conf import settings
import os
from shutil import copyfile

from mar.config import MarManager

from astropy.io import fits

def get_type(header):
    if float(header["EXPTIME"]) == 0:
        return "BIAS"
    elif "bias" in header["IMAGETYP"].lower() or "bias" in header["FILENAME"].lower():
        return "BIAS"
    elif "flat" in header["IMAGETYP"].lower() or "flat" in header["FILENAME"].lower():
        return "FLAT"
    else:
        return "SCI"

def get_field(header):
    try:
        return str(header['OBJECT']).replace(' ', '-')
    except:
        return None

def get_exptime(header):
    try:
        return header['EXPTIME']
    except:
        return None

def get_filter(header):
    try:
        return header['FILTER']
    except:
        return None

def get_filename(name, strip=False):
    if strip: return name.split("/")[-1].replace(".fz", "").replace(".fits", "")
    return name.split("/")[-1]

def check_path(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except:
        pass

def move_file(path, data, tipo, filter=None):
    new_path = settings.ROOTFITS
    new_path = os.path.join(new_path, tipo)

    if tipo == "FLAT" or tipo == "SCI" or tipo == "SEXTRACTOR":
        new_path = os.path.join(new_path, filter)
        check_path(new_path)


    new_path = os.path.join(new_path, data.date().__str__())
    check_path(new_path)

    new_path = os.path.join(new_path, get_filename(path))

    if not os.path.exists(new_path):
        try:
            copyfile(path, new_path)
        except:
            os.system('cp ' + path + ' ' + new_path)

    return new_path

def check_patterns(string, patterns):
    match = False
    for pat in patterns:
        if pat in string:
            match = True
    return match

import os

def absoluteFilePaths(directory):
    """
    Returns a list of absolute file paths for all files in the given directory and its subdirectories.

    Parameters:
    directory (str): The directory to search for files.

    Returns:
    list: A list of absolute file paths.

    Raises:
    FileNotFoundError: If the given directory does not exist.
    NotADirectoryError: If the given directory is not a valid directory.

    Example:
    >>> absoluteFilePaths('/path/to/directory')
    ['/path/to/directory/file1.txt', '/path/to/directory/subdirectory/file2.txt', '/path/to/directory/subdirectory/file3.txt']
    """

    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"'{directory}' is not a valid directory.")

    paths = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            paths.append(os.path.abspath(os.path.join(dirpath, f)))

    return paths

def get_master_path(typ=None):
    if typ is None:
        return settings.ROOTFITS
    if typ == "FLAT":
        return os.path.join(settings.ROOTFITS, "MASTERS", "FLATS")
    if typ == "BIAS":
        return os.path.join(settings.ROOTFITS, "MASTERS", "BIAS")
    if typ == "FRINGE":
        return os.path.join(settings.ROOTFITS, "MASTERS", "FRINGE")

    if typ == "TMP":
        return settings.TMPATH

    if typ == "SEXTRACTOR":
        return os.path.join(settings.ROOTFITS, "SEXTRACTOR")

    if typ == "PROCESSED" or typ == "BPMASK":
        return os.path.join(settings.ROOTFITS, "PROCESSED")

    if typ == "SWARP":
        return os.path.join(settings.ROOTFITS, "SWARP")

    if typ == "SCAMP":
        return os.path.join(settings.ROOTFITS, "SCAMP")

    if typ == "THUMBS":
        return os.path.join(settings.ROOTFITS, "THUMBS")

    if typ == "TILES":
        return os.path.join(settings.ROOTFITS, "TILES")
    
    if typ == "LOGS":
        return os.path.join(settings.ROOTFITS, "LOGS")


def clear_TMP():
    folder = get_master_path('TMP')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))



def generateName(typ, string, startDate=None, endDate=None, ext=".fits", band = None):
    name = string.replace(".fits", "")
    path = get_master_path(typ)

    if typ == "TMP":
        return os.path.join(path, name + ext)

    if typ == "PROCESSED" and band is not None:
        return os.path.join(path, band, name + ext)

    if typ == "BPMASK":
        return os.path.join(path, "BPMASK", name + ext)

    date = str(startDate).replace("-", "") + "-" + str(endDate).replace("-", "")

    if typ == "FLAT" and band is not None:
        path = os.path.join(path, band)

    return os.path.join(path, name + date + ext)


def changeFileName(name, addBefore=None, addAfter=None):
    path = name.rsplit('/' , 1)
    name = path[1]
    path = path[0]

    if addBefore is not None:
        name = addBefore + name

    if addAfter is not None:
        name = name + addAfter

    return os.path.join(path, name)

def getFilePathRootFits(name):
    return os.path.join(settings.ROOTFITS, name)

def removeRootFitsPath(name):
    name = name.replace(settings.ROOTFITS, '')
    if name[-1] == '/':
        name = name[:-1]

    return name

def remove(rm_target : str):
    """Executes remove command. Advantage that may be used with wildcards like *.

    Args:
        rm_target (str): remove target
    """    
    return os.system(f"rm {rm_target}")

def fpack(fpack_target : str, remove_original : bool = False):
    """Executes fpack command. Advantage that may be used with wildcards like *.
    
    Args:
        fpack_target (str): remove target
        remove_original (bool): removes original file
    """
    if os.path.exists(fpack_target + '.fz'):
        rmc = remove(fpack_target + '.fz')
    c = os.system(f"fpack {fpack_target}")
    if remove_original:
        remove(fpack_target)
    return c

def funpack(funpack_target : str, remove_original : bool = False):
    """Executes funpack command. Advantage that may be used with wildcards like *.
    
    Args:
        funpack_target (str): remove target
        remove_original (bool): removes original file
    """
    if os.path.exists(funpack_target.replace('.fz', '')):
        rmc = remove(funpack_target.replace('.fz', ''))
    c = os.system(f"funpack {funpack_target}")
    if remove_original:
        remove(funpack_target)
    return c

def unpacked_hdu(filename):
    """
    Uncompresses an input .fz file.
    Args:
        filename (str): Name of the input .fz file.
    Returns:
        HDUList: The uncompressed HDUList.
    Raises:
        FileNotFoundError: If the input file cannot be found.
        OSError: If the output file cannot be written.
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(f"The input file {filename} cannot be found.")

    packed = fits.open(filename)
    unpacked = fits.hdu.image.PrimaryHDU(data=packed[1].data, header=packed[1].header)
    hdu = fits.hdu.hdulist.HDUList(hdus=[unpacked])
    
    return hdu
