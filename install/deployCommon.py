import os, sys, shutil
import os.path as op
from git import Git


### get source and target dirs and their repos ###

source_dir = op.dirname(os.getcwd())
os.chdir(source_dir)    ## LEAVING INSTALL FOR PARENT DIR

sgit = Git(source_dir)

def abort(msg=None):
   usage = """usage: deployNFS.py deployment_dir http_domain
   Where 
     1) deployNFS.py is in the install subdir 
        of a Divided_Hosts app. 
     2) deployment_dir is has  been initialiized 
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
   http_domain = op.abspath(sys.argv[2])
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
   with open( op.join( source_dir, f) ) as fi:
      txt = fi.read()
   txt = re.sub(
             r'**HTTP_DOMAIN**',
             http_domain,
             txt
         )
   with open( op.join( deployment_dir, f), 'w' ) as fo:
        fo.write(txt)


def getFiles( source_dir, subdir ):
   ''' Make a list of files by recursively searching subdir
       The file paths will assume (but do not contain) a base 
       of op.join(source_dir,subdir).
       Some files excluded, see source code.
   '''

   old_cwd = os.getcwd()
   os.chdir(source_dir)

   filelist = [
      op.join(subdir,f) 
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

def adjustDeploymentDir(
   source_dir,
   target_dir,  # a.k.a. deployment dir
   subdir,
   files,
   copy
):
   ''' Copy files from source_dir to target_dir
       Delete old_files from target_dir if they are not in files
   '''

   old_file_name = op.join( 
                      target_dir, 
                      subdir,
                      '_recently_deployed.py'
                   )

   def adjustFiles(additions,subtractions):
      #   (This adapted from a standard pattern for merging 
      #   two sorted lists.)

      i = j = 0
      while i<len(additions) and j<len(subtractions):
         n = additions[i]
         t = subtractions[j]
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

      while i<len(additions):
         copyfile(additions[i])
         i += 1

      while j < len(subtractions):
         removefile(subtractions[j])
         j += 1

      try:
         with open(old_file_name) as fi:
              old_files = eval( fi.read() )
         assert type(old_files)==type([])
      except:
         abort( 
           "last_deployment.py is not usable\n" +
           "(It should be unstaged in the deployment dir.)"
         ) 

      with open(old_file_name,'w') as fo:
         fo.write( '[' + ','.join(files) + ']' )


