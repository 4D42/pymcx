# -*- coding: utf-8 -*-

def detweight(detp,cfg):
	
	"""
	detw=mcxdetweight(detp,prop)
	
	Recalculate the detected photon weight using partial path data and 
	optical properties (for perturbation Monte Carlo or detector readings)
	
	 author: 
	
	 input:
	     detp: Detected photon. detp must a dictionary 
     prop: optical property list, as defined in the cfg.prop field of mcxlab's input
	
	 output:
	     detw: re-caculated detected photon weight based on the partial path data and media optical property
	
	 
	 License: GPLv3, see http://mcx.space/ for details
	"""
	import numpy as np
	
	Media = cfg['Domain']['Media']
	medianum = len(Media)
	
	if(medianum<=1):
		raise Exception("empty Media list")
	
	if type(detp) is dict:
		
		if not 'w0' in detp:
			detw = 1
		else:
			detw = detp["w0"]
		
		for ind, ppath in enumerate(detp["ppath"]):
			detw = detw * np.exp(-Media[ind+1]["mua"]*ppath)
		
	else:
		raise Exception('the first input must be a dict with a subfield named "ppath"')
	
	return detw
