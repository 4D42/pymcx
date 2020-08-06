# -*- coding: utf-8 -*-

def plotphotons(traj):
	
	"""
	input:
		traj:
			mcx config json file for the simulation as a python dictionary

	output:
		sorted trajectory as dictionary
		
	"""
	
	import matplotlib.pyplot as plt
	from mpl_toolkits.mplot3d import Axes3D
	sorttrag = {}
	
	for pose in traj:
		sorttrag[str(pose[0])] = []
	
	for pose in traj:
		sorttrag[str(pose[0])].append(pose[1:4])
		
	
	fig = plt.figure()
	ax = Axes3D(fig)
	
	for pos in sorttrag:
		pos1 = sorttrag[pos]
		x = [k[0] for k in pos1]
		y = [k[1] for k in pos1]
		z = [k[2] for k in pos1]
		
		ax.plot(x, y, z,'.-')
		
	ax.legend()
	
	return sorttrag