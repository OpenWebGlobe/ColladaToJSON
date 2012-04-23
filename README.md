OpenWebGlobe SDK Collada To JSON Converter
========================

This repository contains the source of the Collada To JSON Converter.
Arbitrary Collada Files (*.dae) can converted into the OpenWebGlobe format for 3d model
description by the python script converter.py

It is planned to create an online platform where users can perform this conversion online.


Command Line Usage
========================
Currently the Converter is executable from commad line:

The ColladaToJson.py is the main file and should be called like this:

ColladaToJson.py -i <inputfile.dae> -c lng,lat,elv

Example: ColladaToJson -i mymodel.dae -c 7.1234,45.243,1200

Note: It is still under development so use it carefully.


Dependencies
========================
The converter uses pycollada to access collada DOM.

License
=======

The i3D OpenWebGlobe SDK is

Copyright (c) 2011 University of Applied Sciences Northwestern Switzerland.
Institute of Geomatics Engineering.

See the file `LICENSE` for details.

