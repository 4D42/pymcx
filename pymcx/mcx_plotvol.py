# -*- coding: utf-8 -*-

def mcxplotvol(data,surface_c = 50,logplot = True):
	import plotly.graph_objects as go
	import plotly.io as pio
	pio.renderers.default = "browser"

	import numpy as np

	if logplot :
		data = np.log10(np.array(data))
	else:
		data = np.array(data)

	datashape = data.shape
	
	X, Y, Z = np.mgrid[0:1:datashape[0]*1j, 0:1:datashape[1]*1j, 0:1:datashape[2]*1j]

	fig = go.Figure(data=go.Volume(
			x=X.flatten(),
			y=Y.flatten(),
			z=Z.flatten(),
			value=data[:,:,:,0].flatten(),
#			isomin=0.01,
#			isomax= data.max(),
			opacity=0.1, # needs to be small to see through all surfaces
			surface_count=surface_c, # number of isosurfaces, 2 by default: only min and max
			))

	fig.show()