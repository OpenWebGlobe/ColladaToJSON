################################################################################
#!c:\python27\python.exe
#
# Server side python execution using WSGI
# Author: Martin Christen, martin.christen@fhnw.ch
#
# Run this script then open your webbrowser and enter:
#   localhost:8000/?a=5
#   localhost:8000/?a=1&b=20
#   localhost:8000/?c=123
#
# or install apache with mod_wsgi and run it directly on your website!
#
# (c) 2012 by FHNW University of Applied Sciences and Arts Northwestern Switzerland
################################################################################

import os.path
import os
import sys
import cgi
from converter import *

################################################################################
message_text = "empty!"
################################################################################

def application(environ, start_response):
    # emit status / headers


    form = cgi.FieldStorage(fp=environ['wsgi.input'],environ=environ)

    #---------------------------------------------------------------------------
    #check if input is correct!
    colladastring = form.getvalue("colladastring")
    lng = float(form.getvalue("lng"))
    lat = float(form.getvalue("lat"))
    elv = float(form.getvalue("elv"))
    filename = form.getvalue("filename")
    prettyprint = form.getvalue("pretty")
    json = convertCollada(filename,colladastring,[lng,lat,elv])

    status = "200 OK"
    headers = [ ('Content-Disposition','attachment'),\
    ('Content-Type', 'application/force-download'),\
    ('Access-Control-Allow-Origin','*'),
    ('Content-Length',str(len(json)))

    ]

    #headers = [('content-type', 'text/plain')]
    start_response(status, headers)


    return json

#-------------------------------------------------------------------------------
# FOR STAND ALONE EXECUTION / DEBUGGING:
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    # this runs when script is started directly from commandline
    try:
        # create a simple WSGI server and run the application
        from wsgiref import simple_server
        print "Running test application - point your browser at http://localhost:8000/ ..."
        httpd = simple_server.WSGIServer(('', 8000), simple_server.WSGIRequestHandler)
        httpd.set_app(application)
        httpd.serve_forever()
    except ImportError:
        # wsgiref not installed, just output html to stdout
        for content in application({}, lambda status, headers: None):
            print content
#-------------------------------------------------------------------------------
			

