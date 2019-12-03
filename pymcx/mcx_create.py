# -*- coding: utf-8 -*-

def create():

	cfgjson = {"Domain": {
							"VolumeFile": "",
							"Dim":    [],
							"OriginType": 1,
							"LengthUnit": 1,
							"Media": [{"mua": 0.00, "mus": 0.0, "g": 0.90, "n": 1.0},
										 {"mua": 0.05, "mus": 10.0, "g": 0.90, "n": 1.0}]
						},
				"Session": {
							"Photons":  1000000,
							"RNGSeed":  -1,
							"ID": "default"
						},
				"Forward": {	"T0": 0.0e+00, "T1": 5.0e-09, "Dt": 5.0e-09},
				"Optode": {
							"Source": {
										"Pos": [21.0, 21.0, 0.0],
										"Dir": [0.0, 0.0, 1.0],
										"Type": "pencil",
										"Param1": [0.0, 0.0, 0.0, 0.0],
										"Param2": [0.0, 0.0, 0.0, 0.0]
										},
							"Detector": [{"Pos": [29.0,  19.0,  0.0], "R": 1.0}]
							},
				"Shapes" : [	{"Grid" : {"Tag" : 1, "Size" : [42,42,42]}}]
				}

	return cfgjson