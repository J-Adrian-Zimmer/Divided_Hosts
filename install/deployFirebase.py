#! /usr/local/bin/python

import os, sys, shutil
import os.path as op

def abort():
   usage = """usage: deployFirebase.py deployment_dir
       Where deployFirebase.py is in the install
       subdir of a Divided_Hosts app. 
       And deployment_dir is has  been initialiized 
       for Firebase deployment.
"""
   print usage
   sys.exit(1)

## get localServe and port from first argument ##

try:
   deployment_dir = op.abspath(sys.argv[1])
except:
   abort()

source_dir = op.abspath(op.join( op.dirname(os.getcwd()), 'get' ))
if not op.isdir(source_dir):
   abort()

public_dir = op.join( deployment_dir, 'public')
if( not (op.isdir(deployment_dir)) and
        op.isdir(public_dir) and
        op.exists(op.join(deployment_dir,'firebase.json'))
):
   abort()

ans = raw_input(
       "Deploy " + source_dir +
       "\nto " + public_dir +
       "\nAnswer with y or n (n is default): "
      )
if ans=='y':
   shutil.rmtree(public_dir)
   shutil.copytree(source_dir,public_dir)
   print "Deploying now"
   os.chdir(op.dirname(public_dir))
   os.system('firebase deploy')
else:
   print "OK, stopping without deploying"

