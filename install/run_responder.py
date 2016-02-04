#! /usr/local/bin/python

import json,sys,os
import os.path as op

env = os.environ

cmd = env['THE_POST_COMMAND'][1:]
exec_path = op.join( '/home/public/post%s.py' % cmd )

if not op.exists(exec_path):
   error( "No %s command can be found" %  cmd )

def get_request():
  return json.dumps( sys.stdin.read() )

def send_response( response, payload ):
  send_me = unicode( json.dumps( 
      { "response": response, 
        "payload": payload,
        "session": ""
      }
  ), 'utf-8')
  print "Status: 200"
  print "Content-Type: text/plain; charset=utf-8"
  print "Content-Length: " + str(len(send_me))
  print
  print send_me

def error(msg):
  send_response( "error", "ERROR: " + msg )
   


try:
   with open( exec_path ) as fi:  exec( fi.read() )
   # should define respond()
except:
   error("Cannot process " + cmd )

try:
  conlen = env['content-length']
except:
  try:
      conlen = env['Content-Length']
  except:
      conlen = env.get('CONTENT-LENGTH',0)


try:
   respond( 
      env, 
      json.loads(sys.stdin.read(conlen)),
      send_response 
   )
except:
   error("Cannot process response.")
   
   


