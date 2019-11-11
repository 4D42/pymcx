# -*- coding: utf-8 -*-

def run(cfg,flag,mcxbin = './mcx'):

	import numpy as np
	import os, json
	
	SID = cfg['Session']['ID']
	f = open(SID+'.json', 'w')
	f.write(json.dumps(cfg, sort_keys=True, indent=2))
	f.close()
	
	
	os.system(mcxbin+' -f '+SID+'.json '+flag)