import numpy as np 

def coordinate2str(coord):
	'''
	[y1, y2, x1, x2] to [x1:x2,y1:y2] with iraf indexes (starting at 1)
	'''
	coord = np.array(coord)
	if len(coord) != 4:
		raise Exception("Coordinate array length is != 4")

	coord = "[" + str(coord[2] + 1) + ":" + str(coord[3]) + "," + str(coord[0] + 1) + ":" + str(coord[1]) + "]"
	return coord

def str2coordinate(string):
	'''
	[x1: x2, y1: y2] to [y1, y2, x1, x2] with iraf indexes (starting at 0)
	'''

	try:
		string = string.strip(' ').strip("[").strip("]").split(",")
		x = np.array(string[1].split(':'), dtype=np.int16)
		y = np.array(string[0].split(':'), dtype=np.int16)

		x[0] = x[0] - 1
		y[0] = y[0] - 1
		coord = np.concatenate((x, y), axis=None)

		return coord
	except:
		raise Exception("Error converting str to coord")
