__author__ = 'benjamin.loesch'
from daeConverter import *
import glob, os
import unzip
try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree
import re
import sys
from zipfile import BadZipfile, ZipFile
import daeConverter
import zipfile
import shutil
import htmlCreator
sys.path.append("/var/www/converter/scripts/")

class kmzConverter:
    def __init__(self, verbose = True, percent = 10):
        self.verbose = verbose
        self.percent = percent


    def convertKmz(self, file, dir, dirout,fname):

        #extract the zip file to a folder
        un = unzip.unzip()
        un.extract(file,dir)

        nrkml = 0;
        nrcollada = 0

        for root, dirs, files in os.walk(dir):
            for name in files:
                if name.endswith((".kml")):
                    kmlfile = open(os.path.join(root, name),'r')
                    pos_ori = self.extractLocation(kmlfile)
                    kmlfile.close()
                    nrkml = nrkml+1

                if name.endswith((".dae")):
                    colladafilepath = os.path.join(root, name)
                    (path,name) = os.path.split(colladafilepath)
                    nrcollada = nrcollada+1

        if(nrkml==0):
            return "error: no georeference info in zip file. Try to convert the *dae file separately !"

        if(nrkml>1):
            return "error: more than one kml file in zipfile. Convert multiple models separately !"

        if(nrcollada==0):
            return "error: no *.dae file found in zip file !"

        if(nrcollada>1):
            return "error: multiple collada files in zip file. Convert multiple models separately !"



        convertCollada(colladafilepath,[float(pos_ori[0]),float(pos_ori[1]),float(pos_ori[2])],dirout) #writes the jsonfile into the extracted folder structure



        #copy all images in the output folder
        self.copyimages(dir,dirout,'jpg', 'png','gif','json') #add supporting filetypes here...
        dirred = dir[:-5]

        for jsonfile in glob.glob(dirout+"/*.json"):
            #create the demo html file
            (path,name) = os.path.split(jsonfile)
            htmlCreator.createHTML(name,float(pos_ori[0]),float(pos_ori[1]),float(pos_ori[2]),dirout+'/modeldemo.html')


        #store the jsonfile in a new zip file
        self.zipper(dirout,dirred+'/jsonzip.zip')
        return dirred+"/jsonzip.zip"


    def copyimages(self, dirsrc,dirdest,*args):
        for file in os.listdir(dirsrc):
            dirfile = os.path.join(dirsrc, file)
            if os.path.isfile(dirfile):
                if len(args) == 0:
                    fileList.append(dirfile)
                else:
                    if os.path.splitext(dirfile)[1][1:] in args:
                        shutil.copyfile(dirfile, os.path.join(dirdest, file))
            elif os.path.isdir(dirfile):
                #print "Accessing directory:", dirfile
                self.copyimages(dirfile,dirdest, *args)
            else:
                pass



    # Function written by TomPayne camp2camp from
    # https://github.com/OpenWebGlobe/WebViewer/blob/minimal-example/scripts/kmz-extract-location.py
    def extractLocation(self, kmlfile):

        et = ElementTree.parse(kmlfile)
        namespace = re.match(r'\{(.*)\}', et.getroot().tag).group(1)
       # print 'Location:'
       # for location in et.findall('//{%s}Location' % namespace):
       #     print '\tLatitude: %s' % location.find('{%s}latitude' % namespace).text
       # print '\tLongitude: %s' % location.find('{%s}longitude' % namespace).text
       # print '\tAltitude: %s' % location.find('{%s}altitude' % namespace).text
       # print 'Orientation:'
       # for orientation in et.findall('//{%s}Orientation' % namespace):
       #     print '\tRoll: %s' % orientation.find('{%s}roll' % namespace).text
       # print '\tTilt: %s' % orientation.find('{%s}tilt' % namespace).text
       # print '\tHeading: %s' % orientation.find('{%s}heading' % namespace).text
        for location in et.findall('.//{%s}Location' % namespace):
            lng = location.find('{%s}longitude' % namespace).text
            lat = location.find('{%s}latitude' % namespace).text
            elv = location.find('{%s}altitude' % namespace).text
        for orientation in et.findall('.//{%s}Orientation' % namespace):
            yaw = orientation.find('{%s}heading' % namespace).text
            pitch = orientation.find('{%s}tilt' % namespace).text
            roll = orientation.find('{%s}roll' % namespace).text

        return [lng,lat,elv,yaw,pitch,roll]


    def zipper(self, dir, zip_file):
        zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
        root_len = len(os.path.abspath(dir))
        for root, dirs, files in os.walk(dir):
            archive_root = os.path.abspath(root)[root_len:]
            for f in files:
                fullpath = os.path.join(root, f)
                archive_name = os.path.join(archive_root, f)
                #print f
                zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
        zip.close()
        return zip_file



