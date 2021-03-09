# -*- coding: utf-8 -*-

def writevolbin(vol,filename):
	
	"""
	detw=mcxdetweight(detp,prop)
	
	writing the volum in a binary file for mcx
	
	 author: maxime baillot
	
	 input:
		 vol: 3D volume of medium valu (0,1,2,etc...)
		 filename: Name of the bin file
     
	 
	 License: GPLv3, see http://mcx.space/ for details
	"""
	import numpy as np
	
	fname = filename+'.bin'

	f = open(fname, 'wb')
	dmedium = np.array(vol,int)
	f.write(dmedium)
	f.close()
