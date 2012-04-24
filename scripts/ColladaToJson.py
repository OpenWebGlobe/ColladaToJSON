#!/usr/bin/python
import sys, getopt
import os.path
import os
import sys
import cgi

sys.path.append("/var/www/converter/scripts/")

from daeConverter import *
import string
import zipfile
from cStringIO import StringIO
import time
import kmzConverter
import shutil



if __name__ == '__main__':

    inputfile = ''
    outputfile = ''
    centerneeded = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:c:center:",["ifile=","center="])
    except getopt.GetoptError:
        print "Wrong parameters...\n"
        print "Usage: ColladaToJson.py -i <inputfile.dae> -c lng,lat,elv\nExample: ColladaToJson -i mymodel.dae -c 7.1234,45.243,1200"
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "Usage: ColladaToJson.py -i <inputfile.dae> -c lng,lat,elv\nExample: ColladaToJson -i mymodel.dae -c 7.1234,45.243,1200"
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-c", "--center"):
            center = arg.split(',')
            center[0] = float(center[0])
            center[1] = float(center[1])
            center[2] = float(center[2])

    print 'Input file is "', inputfile+'"'


    #check if it's a zip file..
    if inputfile[-3:]=='dae':
        try:
            center
        except:
            print 'No center defined!'
            print "Usage: ColladaToJson.py -i <inputfile.dae> -c lng,lat,elv\nExample: ColladaToJson -i mymodel.dae -c 7.1234,45.243,1200"
            sys.exit(2)
        convertedfilepath = convertCollada(inputfile,center,os.getcwd())

        print "\n Generated model: "+convertedfilepath

    elif inputfile[-3:]=='kmz' or inputfile[-3:]=='zip':
        os.mkdir(os.getcwd()+'/ConversionResult', 0777)
        kmzconv = kmzConverter.kmzConverter();
        convertedfilepath = kmzconv.convertKmz(inputfile,os.getcwd()+'/tmp',os.getcwd()+'/ConversionResult',inputfile)
        print "\n Generated model zip: "+convertedfilepath
    else:
        print "filetype not suported"


    #delete the two folders
    shutil.rmtree(os.getcwd()+'\\tmp')
    shutil.rmtree(os.getcwd()+'\\ConversionResult')



