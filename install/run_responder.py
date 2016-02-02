#! /usr/local/bin/python

import json,sys,os
import os.path as op

env = os.environ

exec_path = op.join( 
              '/home/public/post',
              env['PATH_INFO'] + '.py'
            )

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
   

if not op.exists(exec_path):
   error( exec_path + " does not exist." )

try:
   with open( exec_path ) as fi:  exec( fi.read() )
   # should define respond()
except:
   error("Cannot process " + env['PATH_INFO'][1:] )

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
   
   


