import os 
import mar 

from mar.config import MarManager
from mar.wrappers.terminal import runCommand

marConf = mar.AttributeDict(mar.env.marConf.Thumbs)

def make_thumb(inp, output):
	"""
    Create a thumbnail image from a FITS file.
    
    Parameters:
    -----------
    inp : str
        The input FITS file.
    output : str
        The output thumbnail file.
        
    Returns:
    --------
    None
    """
	res = runCommand(f"fitspng -s {marConf.SHRINK} -f {marConf.TYPE} -f0 5 -o {output} {inp}", timeout=marConf.TIMEOUT)
	
	if res == 0:
		MarManager.INFO("Thumb made with sucess.")
	else:
		MarManager.WARN("Failed to make thumb.")


def delete_file(file):
	"""
	Delete a file from the file system.

	Parameters:
	-----------
	file : str
		The path of the file to delete.

	Returns:
	--------
	None
	"""
	res = os.system(f"rm {file}")