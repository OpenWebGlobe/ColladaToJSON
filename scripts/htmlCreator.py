__author__ = 'benjamin.loesch'

import string
import os


def createHTML(jsonfilename,lng,lat,elv,outpath):

    htmltemplate = open(os.getcwd()+'/htmltemplate.txt','r')
    htmltemplatestring =  string.Template(htmltemplate.read())
    htmltemplate.close()

    filledstring = htmltemplatestring.substitute(modelpath="'"+jsonfilename+"'",lng=lng,lat=lat,elv=elv)

    file = open(outpath,'w')
    file.write(filledstring);
    file.close()








