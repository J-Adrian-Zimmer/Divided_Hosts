The `install` Subdir
----------------

The Python files in this directory are of three kinds

1. `serveYOS.py` which runs Your Own Server 1. `install...` files
which install application files (that is get and post files) to NFS,
FA, or FH or simple static (that is get files) files to Firebase.
Installation is from the current working directory.

1. `utility` files which must be manually placed into one of
NearlyFreeSpeech, Heroku, or Openshift as appropriate so that the
installed application files will work appropriately.

The `install...` programs put get files on NFS or Firebase and post
Python files on NFS, Heroku, or Openshift.    
