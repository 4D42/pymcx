# -*- coding: utf-8 -*-

def run(cfg, flag, mcxbin = 'default', datadict = False):

	"""
	input:
		cfg:
			mcx config json file for the simulation as a python dictionary
		
		flag:
			flag for runing mcx
			
		mcxbin:
			path for the mcx binary

	output:
		mch_data:
	"""

	import os
	import json
	import pymcx as mcx


	SID = cfg['Session']['ID']


	f = open(SID+'.json', 'w')
	f.write(json.dumps(cfg, sort_keys=True, indent=2))
	f.close()


	if mcxbin == 'default':
		if os.name == "posix":
			 mcxbin = './mcx'
		else:
			mcxbin = '.\mcx.exe'

	os.system(mcxbin+' -f '+SID+'.json '+flag)


	mch = []
	mc2 = []

	if os.path.isfile(SID+'.mch'): mch = mcx.loadmch(SID+'.mch', datadict = datadict)

	if os.path.isfile(SID+'.mc2'):

		nbstep = round((cfg["Forward"]["T1"] - cfg["Forward"]["T0"])/cfg["Forward"]["Dt"])

		if "Dim" in cfg["Domain"] and cfg["Domain"]["Dim"] != []:
			dt = cfg["Domain"]["Dim"] + [nbstep]

		elif "Shapes" in cfg:
			for find in cfg["Shapes"]:
				if "Grid" in find:
					dt = find["Grid"]["Size"] + [nbstep]


		mc2 = mcx.loadmc2(SID+'.mc2',dt)


	return mch, mc2