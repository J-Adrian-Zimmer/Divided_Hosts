import os, sys, shutil, json
import os.path as op
from git import Git

### get source and development dirs and their repos ###

source_dir = op.dirname(os.getcwd())
os.chdir(source_dir)    ## LEAVING INSTALL FOR PARENT DIR

sgit = Git(source_dir)

def abort(msg=None):
   usage = """usage: deploy{NFS|FH|FO}.py deployment_dir http_domain
   Where 
     1) deployNFS.py is in the install subdir 
        of a Divided_Hosts app. 
     2) deployment_dir is has  been initialized 
        for NFS deployment.
     3) http_domain is the domain name for responder
        files including an http or https prefix"""
   
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

try:
   http_domain = sys.argv[2]
   assert http_domain[:4]=="http"
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

def copyfile(f):
    shutil.copyfile(
      op.join( source_dir, f),
      op.join( deployment_dir, f)
    )

def removefile(f):
   os.remove( op.join( deployment_dir, f) )

def filterfile(f):
   import re
   with open( op.join(source_dir,f) ) as fi:
      txt = fi.read()
   with open( op.join(deployment_dir,f), 'w' ) as fo:
      fo.write(
          re.sub(
             r'http://localhost',
             http_domain,
             txt
      )   )

def adjustFiles(additions,old_additions,copy):
   ''' Copies or deletes files.  The copy parameter allows for straight or filtered copying.
   ''' 

   #   (This adapted from a standard pattern for merging 
   #   two sorted lists.)

   i = j = 0
   while i<len(additions) and j<len(old_additions):
      n = additions[i]
      t = old_additions[j]
      if n<t:
         copy(n)
         i += 1
      elif n>t:  # old file t is no longer in use
         removefile(t)
         j += 1
      else:  # n==t
         copy(n)
         # skipping over t
         i += 1; j += 1

   while i<len(additions):
      copy(additions[i])
      i += 1

   while j < len(old_additions):
      removefile(old_additions[j])
      j += 1


def getFiles( rootdir ):
   ''' Make a list of files by recursively searching rootdir
       The file paths will assume (but do not contain) a base 
       of op.join(source_dir,rootdir).
       Some files excluded, see source code.
   '''

   old_cwd = os.getcwd()
   os.chdir( op.join(source_dir, rootdir) )

   filelist = [
      op.join(rootdir,dir,f) 
        for (dir,_, files) in os.walk('.')
           for f in files
              if ( f[0]!='.' and 
                   f[0]!='_' and
                   f[-4:]!='.pyc' and
                   f[-4:]!='.swp' and
                   f[-3:]!='.md'
                 )
   ]

   os.chdir(old_cwd)
   return filelist

def adjustDeploymentDir( subdir, copy ):
   ''' Copy subdir's files from source_dir to deployment_dir.  Delete old_files from deployment_dir if they are not in source_dir.
   '''

   ### prepare ###

   remembered_path = op.join( 
                      deployment_dir, 
                      'last_deployment.py'
                   )
   try:
      with open(remembered_path) as fi:
           remembered = json.loads( fi.read() )
   except:
      abort( 
        "last_deployment.py is not usable\n" +
        "(It should be unstaged in the deployment dir.)"
      )
       
   new_files = getFiles(subdir)
   deployed_files = remembered['Divided_Hosts'][subdir]
   
   ### do ###
   
   adjustFiles(new_files, deployed_files,copy)
    
   ### record ###

   remembered['Divided_Hosts'][subdir] = new_files 
   with open(remembered_path,'w') as fo:
      fo.write( json.dumps(remembered) )


