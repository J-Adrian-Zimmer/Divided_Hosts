#! /usr/local/bin/python

import os, sys, shutil
import os.path as op
from git import Git

### get source and target dirs and their repos ###

source_dir = op.dirname(os.getcwd())
os.chdir(source_dir)    ## LEAVING INSTALL FOR PARENT DIR

sgit = Git(source_dir)

def abort(msg=None):
   usage = """usage: deployNFS.py deployment_dir
   Where 
     1) deployNFS.py is in the install subdir 
        of a Divided_Hosts app. 
     2) deployment_dir is has  been initialiized 
        for NFS deployment. """
   
   if msg:
      print msg
   else:
      print usage
   sys.exit(1)


try:
   deployment_dir = op.abspath(sys.argv[1])
except:
   abort()
dgit = Git(deployment_dir)



### are source_dir and deployment_dir as expected? ###

def has_get_post(adir):
  return op.isdir(
            op.join(adir,'get')
         ) and op.isdir(
            op.join(adir,'post')
         )

if not (
     has_get_post(source_dir)  and
     has_get_post(deployment_dir)
):
   abort()



### make sure there are no uncommited staged changes ###

if (  # string listing filenames of those staged
      # files with differences from the HEAD
      # is NOT empty
    sgit.diff_index('--name-only','--cached','HEAD')!=u''
):
  abort( "Commit your staged changes first" )




### want to go through with this? ###

ans = raw_input(
       "Deploy " + source_dir +
       "\nto " + deployment_dir +
       "\nAnswer with y or n (n is default): "
      )
if ans!='y':
   abort( "OK, stopping without deploying" )


       
### get last_deployment and cur_deployment lists of files ###


def addFiles():
   
   desired_files = [] 
   for (dir,dirs, files) in os.walk('.'):
      if dir=='.':
         for d in dirs: 
            if d not in ['py','get','post']:
               dirs.remove(d)
            # cannot reassign dirs, gotta remove
            # to get the magic avoidance of some dirs
      else: # don't want any root level files
         for f in files:
            if ( f[0]!='.' and 
                 f[0]!='_' and
                 f[-4:]!='.pyc' and
                 f[-3:]!='.md'
            ):
               desired_files.append( op.join(dir,f) )
   return desired_files

cur_deployment = addFiles()
cur_deployment.sort()

os.chdir(deployment_dir)  # NOTICE CHANGE OF DIR AND REPO

try:
   with open('last_deployment.py') as fi:
        exec( fi.read() )
   assert type(last_deployment)==type([])
except:
   abort( 
     "last_deployment.py is not usable\n" +
     "(It should be unstaged in the deployment dir.)"
   ) 


### copy what's in cur_deployment and delete
### what's in last_deployment but not cur_deployment

#   (This adapted from a standard pattern for merging 
#   two sorted lists.)

def copyfile(f):
    shutil.copyfile(
      op.join( source_dir, f),
      op.join( deployment_dir, f)
    )

def removefile(f):
   os.remove( op.join( deployment_dir, f) )

i = j = 0
while i<len(cur_deployment) and j<len(last_deployment):
   n = cur_deployment[i]
   t = last_deployment[j]
   if n<t:
      copyfile(n)
      i += 1
   elif n>t:
      removefile(t)
      j += 1
   else:  # n==t
      copyfile(n)
      # skipping over t
      i += 1; j += 1

while i<len(cur_deployment):
   copyfile(cur_deployment[i])
   i += 1

while j < len(last_deployment):
   removefile(last_deployment[j])
   j += 1




### stage and commit the changes ###

dgit.add('-A','.')
dgit.commit(
      '-m',
      'Deploying\n\n   ' +
         '\n   '.join(cur_deployment)
)



### push to NFS ###

dgit.push('nfs','master')



### update last_deployment.py ###

with open(
   op.join(deployment_dir,'last_deployment.py','w')
) as fo:
   fo.write( 'last_deployment = [' +
             ','.join( cur_deployment ) +
             ']'
           )
