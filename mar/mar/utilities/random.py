import random

def randname():
    """
    Create a random string useful to create a temporal file names

    Parameters
    ----------

    Returns
    -------
    Random string : format  xxxxx_xxxxx

    """
    random.seed()
    str1 = str(random.randint(0, 10000))
    random.seed()
    str2 = str(random.randint(0, 10000))
    return str2 + "_" + str1

def get_filename(name, strip=False):
    if strip: return name.split("/")[-1].replace(".fz", "").replace(".fits", "")
    return name.split("/")[-1]
