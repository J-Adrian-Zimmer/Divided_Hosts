#! /usr/local/bin/python

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import os.path as op
import sys,os


def abort():
   usage = """usage: serveYOS.py -port 
       where serveYOS.py is in the install
       subdir of a Divided_Hosts app
       change - to + for unrestricted service
"""
   print usage
   sys.exit(1)

## get localServe and port from first argument ##

try:
   where = sys.argv[1]
except:
   abort()

if where[0]=='+':
   localServe = False
   ip = '0.0.0.0'
elif where[0]=='-':
   ip = '127.0.0.1'
   localServe = True
else:
   abort()

try:
   port = int(where[1:])
except;
   abort()

##  root of public directory should be the get dir

root = op.abspath('../get')
if op.isdir('../get'):
   os.chdir(root)
else:
   abort()


## start server ##

httpd = HTTPServer((ip,port), SimpleHTTPRequestHandler)
      ## server needs to know 
      ##    what ip to serve from
      ##    what port to serve from
      ##    what handler class to use when making a handler

print 'Starting %s service on port %d\nfrom root dir %s' % (
         'local' if localServe else 'global',  
         port,  
         root
      )
print '...'

httpd.serve_forever() 



