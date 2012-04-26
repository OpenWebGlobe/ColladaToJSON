__author__ = 'benjamin.loesch'

import string
import os
import urllib

def createHTML(jsonfilename,lng,lat,elv,outpath):


   htmltemplate = urllib.urlopen('http://www.openwebglobe.org/converter/scripts/html.txt')

   htmltemplatestring =  string.Template(htmltemplate.read())
   htmltemplate.close()

   filledstring = htmltemplatestring.substitute(modelpath="'"+jsonfilename+"'",lng=lng,lat=lat,elv=elv)

   file = open(outpath,'w')
   file.write(filledstring);
   file.close()








