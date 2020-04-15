"""
author: Shih-Cheng Tu
email: mrtoastcheng@gmail.com

"""

def loadmc2(path, dimension):

	"""
	input: 
		path: 
			the file path of the .mc2 file.

		dimension: 
			an array to specify the output data dimension
			normally, dim=[nx,ny,nz,nt]

	output: 
		data: 
			the output MCX solution data array, in the
			same dimension specified by dim

	"""
	import numpy as np
	from struct import unpack

	f = open(path, 'rb')
	data = f.read()
	data = unpack('%df' % (len(data)/4), data)
	data = np.asarray(data).reshape(dimension, order='F')

	return data
