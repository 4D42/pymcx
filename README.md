# pymcx

Python package for [MCX](http://mcx.space/) .

The way the package work is as fallow. It run mcx externally and use Json file as config. It is like doing,

	./mcx -f cfg.json *flags*

The advantage is that it will create a default cfg and load all the data that is given back by mcx so it can be processed directly after in Python.

*All the functions can also be used separately.*

## package information

### structure


### functions
- **loadmch() :** load .mch file and output the detected photons data as an array or a dictionary
- **loadmc2() :**
- **create()**
- **run()**

## How to use it

### Example

```Python

import pymcx as mcx

cfg = mcx.create() #create a default config dictionary

cfg["Session"]["Photons"] = 1e6
cfg["Optode"]["Detector"] = [{"Pos": [29.0,  19.0,  0.0], "R": 1.0}]

data = mcx.run(cfg)

```

To have more information read the Json part of the MCX [readme](http://mcx.space/wiki/index.cgi?Doc/README). The cfg variable is a python dictionary that look like a Json structure.
