

def loadmch(fname,format = 'f',endian = 'ieee-le',datadict = False):

	"""
	input:
		fname:
			the file path of the .mch file.

	output:
		mch_data:
			the output detected photon data array
			data has at least M*2+2 columns (M=header.maxmedia), the first column is the
			ID of the detector; columns 2 to M+1 store the number of
			scattering events for every tissue region; the following M
			columns are the partial path lengths (in mm) for each medium type;
			the last column is the initial weight at launch time of each detecetd
			photon; when the momentum transfer is recorded, M columns of
			momentum tranfer for each medium is inserted after the partial path;
			when the exit photon position/dir are recorded, 6 additional columns
			are inserted before the last column, first 3 columns represent the
			exiting position (x/y/z); the next 3 columns are the dir vector (vx/vy/vz).
			in other words, data is stored in the follow format
			[detid(1) nscat(M) ppath(M) mom(M) p(3) v(3) w0(1)]

		header:
			file header info, a dictionary that contains
			version,medianum,detnum,recordnum,totalphoton,detectedphoton,
			savedphoton,lengthunit,seed byte,normalize,respin]

		photonseed:
			(optional) if the mch file contains a seed section, this
			returns the seed data for each detected photon. Each row of
			photonseed is a byte array, which can be used to initialize a
			seeded simulation. Note that the seed is RNG specific. You must use
			the an identical RNG to utilize these seeds for a new simulation.
	"""
	import numpy as np
	from struct import unpack
	
	def fread(fileid , N, Type):
		"""
		Small utility function to read and unpack databits
		
		fileid:Id of the file opend with open()
		N: number of Characters to read
		Type: the type of the Character to read
		"""
		
		if Type == 'c' or Type == 'b' or Type == 'B' or Type == '?':
			Nb = 1
		elif Type == 'h' or Type == 'H' :
			Nb = 2
		elif Type == 'i' or Type == 'I' or Type == 'l' or Type == 'L' or Type == 'f':
			Nb = 4
		elif Type == 'q' or Type == 'Q' or Type == 'd' :
			Nb = 8
		else :
			raise Exception("Type unknow")
		
		# exemple version = unpack('I', fid.read(4))[0] read a uint
		if N == 1:
			return unpack(Type, fileid.read(Nb))[0]
		else :
			return unpack(str(N)+Type, fileid.read(N*Nb))


	try:
		fid = open(fname, 'rb')
	except:
		raise Exception("Could no open the given file name "+fname)


	data = []
	header = []
	photon_seed = []


	while True:
		
		magicheader = fid.read(4) # a char is 1 Bytes
		
		if not magicheader:
			break
		elif magicheader != b'MCXH':
			fid.close()
			raise Exception("It might not be a mch file!")

		version = fread(fid,1,'I')


		assert version == 1, "version higher than 1 is not supported"


		maxmedia = fread(fid,1,'I')
		detnum = fread(fid,1,'I')
		colcount = fread(fid,1,'I')
		totalphoton = fread(fid,1,'I')
		detected = fread(fid,1,'I')
		savedphoton = fread(fid,1,'I')
		unitmm = fread(fid,1,'f')
		seedbyte = fread(fid,1,'I')
		normalizer = fread(fid,1,'f')
		respin = fread(fid,1,'i')
		srcnum = fread(fid,1,'I')
		savedetflag = fread(fid,1,'I')
		junk = fread(fid,2,'i')


		detflag = np.asarray(list(bin(savedetflag & (2**8-1))[2:]),'int')
		if endian == 'ieee-le': detflag = detflag[::-1]  #flip detflag left to right
		datalen = np.asarray([1, maxmedia, maxmedia, maxmedia, 3, 3, 1])
		datlen = detflag*datalen[0:len(detflag)]


		dat = fread(fid,(colcount*savedphoton),format)
		dat = np.asarray(dat).reshape(savedphoton, colcount)


		if savedetflag and len(detflag)>2 and detflag[2]>0:
			dat[:,sum(datlen[0:2]):sum(datlen[0:3])] = dat[:,sum(datlen[0:2]):sum(datlen[0:3])]*unitmm
		elif savedetflag == 0:
			dat[:,1+maxmedia:(2*maxmedia)]=dat[:,1+maxmedia:(2*maxmedia)]*unitmm


		#make the data as a dictionary
		if datadict:
			if savedetflag:
				data_dic = [{} for x in range(savedphoton)]
				for photonid in range(savedphoton):
					if len(detflag)>0 and detflag[0] != 0 : data_dic[photonid]["detid"] = dat[photonid][0]
					if len(detflag)>1 and detflag[1] != 0 : data_dic[photonid]["nscat"] = dat[photonid][datlen[0]:1+datlen[1]]
					if len(detflag)>2 and detflag[2] != 0 : data_dic[photonid]["ppath"] = dat[photonid][sum(datlen[0:2]):sum(datlen[0:3])]
					if len(detflag)>3 and detflag[3] != 0 : data_dic[photonid][ "mom"] = dat[photonid][sum(datlen[0:3]):sum(datlen[0:4])]
					if len(detflag)>4 and detflag[4] != 0 : data_dic[photonid]["p"] = dat[photonid][sum(datlen[0:4]):sum(datlen[0:5])]
					if len(detflag)>5 and detflag[5] != 0 : data_dic[photonid]["v"] = dat[photonid][sum(datlen[0:5]):sum(datlen[0:6])]
					if len(detflag)>6 and detflag[6] != 0 : data_dic[photonid]["w0"] = dat[photonid][-1]

			elif savedetflag == 0:
				data_dic = [{"detid": photon[0],
							  "nscat": photon[1:1+maxmedia],
							  "ppath": photon[1+maxmedia:1+2*maxmedia],
							  "mom": photon[1+2*maxmedia:1+3*maxmedia],
							  "p": photon[-7:-4:1], "v": photon[-4:-1:1],
							  "w0": photon[-1]} for photon in dat]

			del dat
			dat = np.asarray(data_dic)


		data.append(dat)


		# if "save photon seed" is True
		if seedbyte > 0:

#			seeds = unpack('%dB' % (savedphoton*seedbyte), fid.read(savedphoton*seedbyte))
			seeds = fread(fid,(savedphoton*seedbyte),'B')
			photon_seed.append(np.asarray(seeds).reshape((seedbyte,savedphoton), order='F'))


		if respin > 1: totalphoton *= respin


		header = {'version': version,
					'medianum': maxmedia,
					'detnum': detnum,
					'recordnum': colcount,
					'totalphoton': totalphoton,
					'detectedphoton': detected,
					'savedphoton': savedphoton,
					'lengthunit': unitmm,
					'seedbyte': seedbyte,
					'normalizer': normalizer,
					'respin': respin,
					'srcnum': srcnum,
					'savedetflag': savedetflag}




	fid.close()


	data = np.asarray(data).squeeze()


	if seedbyte > 0:
		photon_seed = np.asarray(photon_seed).transpose((0,2,1)).squeeze()


	return data, header, photon_seed
