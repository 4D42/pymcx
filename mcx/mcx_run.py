# -*- coding: utf-8 -*-

def run(cfg,flag,mcxbin = './mcx'):
	
	import numpy as np
	import os, json

	f = open(name+'.json', 'w')
	f.write(json.dumps(cfg, sort_keys=True, indent=2))
	f.close()

	os.system(mcxbin+' -f '+cfg["Session"]["ID"]+'.json '+flag)