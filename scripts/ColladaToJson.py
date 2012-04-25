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

    if(len(sys.argv)<2):
        print "Wrong parameters...\n"
        print "Usage: ColladaToJson.py -i <inputfile.dae> -c lng,lat,elv\nExample: ColladaToJson -i mymodel.dae -c 7.1234,45.243,1200"
        sys.exit(2)

    try:
        dir = 'ConvertedModel_'+str(time.time())
        dir = dir[:-3]
        diroriginal = dir+'/temp'
        dirnew = dir+'/out'
        os.mkdir(dir, 0777)
        os.mkdir(diroriginal, 0777)
        os.mkdir(dirnew, 0777)

        #check if it's a zip file..
        if inputfile[-3:]=='dae':
            try:
                center
            except:
                print 'No center defined!'
                print "Usage: ColladaToJson.py -i <inputfile.dae> -c lng,lat,elv\nExample: ColladaToJson -i mymodel.dae -c 7.1234,45.243,1200"
                sys.exit(2)
            convertedfilepath = convertCollada(inputfile,center,dir)

            print "\n Generated model: "+convertedfilepath

        elif inputfile[-3:]=='kmz' or inputfile[-3:]=='zip':
            kmzconv = kmzConverter.kmzConverter();
            convertedfilepath = kmzconv.convertKmz(inputfile,diroriginal,dirnew,inputfile)
            print "\n Generated model zip: "+convertedfilepath
        else:
            print "filetype not suported"

        if convertedfilepath.find('error')>0:
            print convertedfilepath
            sys.exit(2)
            os.rmdir(dir)

        shutil.rmtree(diroriginal)
        shutil.rmtree(dirnew)
        print '\n\n Conversion Succesful\n See the converted model in new folder: '+dir
    except:
        print sys.exc_info()[1]
        sys.exit(2)





