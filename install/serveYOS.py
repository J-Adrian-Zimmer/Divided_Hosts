#! /usr/local/bin/python

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import os.path as op
import sys,os,urlparse,json
env = os.environ

def abort():
   usage = """usage: serveYOS.py -port 
       where serveYOS.py is in the install
       subdir of a Divided_Hosts app
       change - to + for unrestricted service
"""
   print usage
   sys.exit(1)

class _Bunch:
   '''
   The _Bunch class makes a Python class from a dict
   It enables jsonIn to return an object rather than a dict
   '''
   def __init__(self, adict):
        self.__dict__.update(adict)


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
except:
   abort()






## helper functions 
##   These require a handler instance.

def make_send_response( handler ):
  def send_response(response,payload): 
     send_me = unicode( json.dumps( 
         { "response": response, 
           "payload": payload,
           "session": ""
         }
     ), 'utf-8')
     handler.send_response(200)
     handler.send_header( 
         "Content-Type", 
         "text/plain; charset=utf-8" 
     )
     handler.send_header(
          'content-length',
          str(len(send_me))
     )
     handler.end_headers()
     handler.wfile.write(send_me)
  return send_response

def error(handler,msg):
  make_send_response(handler)( 
           "error", 
           "ERROR: " + msg 
  )
   
def respond_to_post_request(handler,cmd):
   
   try:                           # get the desired .py #
      with open(cmd+'.py') as fi: 
          exec_me = fi.read()
   except:
      error(handler, "No %s command can be found" %  cmd )

   try:              # get respond function from exec_me #
      exec(exec_me)
   except:
      error(handler, "Difficulty with %s.py" % cmd)

   try:            # get the length of the incoming json #
     conlen = handler.headers['content-length']
   except:
     conlen = 0

   try:              # make incoming json into an object #
     obj =  _Bunch(
               json.loads(
                  handler.rfile.read(int(conlen))
            )  )
     print "incoming payload:" + obj.payload
   except:
     error( handler, "Cannot process incoming json" )
       
   try:                 # evaluate and send the response #
      respond( 
         env,
         obj,
         make_send_response(handler)
      )
   except:
      error(handler,"Cannot process response.")
    
     


## extend SimpleHTTPRequestHandler for POST requests ##

class PostHandler (SimpleHTTPRequestHandler):

    def do_POST(self):
        os.chdir( '../post' )
        scheme,netloc,path,params,query,fragment = \
                         urlparse.urlparse(self.path)
        cmd = path[1:] 
        env['THE_POST_COMMAND'] = cmd 
        respond_to_post_request(self, cmd )
        print 'RESPONDED'
        os.chdir('../get')




## start server ##

httpd = HTTPServer((ip,port), PostHandler)
      ## server needs to know 
      ##    what ip to serve from
      ##    what port to serve from
      ##    what handler class to use when making a handler

root = op.abspath('../get')
if op.isdir('../get'):
   os.chdir(root)
else:
   abort()

print 'Starting %s service on port %d\nfrom root dir %s' % (
         'local' if localServe else 'global',  
         port,  
         root
      )
print '...'

httpd.serve_forever() 



