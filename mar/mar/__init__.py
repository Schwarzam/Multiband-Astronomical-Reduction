from .main import * 

from . import image
from . import reduction
from . import config
from . import utilities
from . import wrappers

'''
updatehead.py -i /mnt/public/t80s_scripts/reduction/config/t80cam[or _mode5].yaml /path/to/img
imgclassify.py /path/to/img
insertdb.py /path/to/img
createthumb.py /path/to/img
ln -s /path/to/img /path/to/thumbnails/$(echo $img | cut -d/ -f5)
'''

"""
PATH=/bin:/Users/gustavo/.iraf/bin:${PATH}:/Users/gustavo/.iraf/bin:${PATH}
export PATH
"""

