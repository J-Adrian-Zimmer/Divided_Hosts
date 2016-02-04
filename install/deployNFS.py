#! /usr/local/bin/python

with open('deployCommon.py') as fi:
   exec( fi.read() )

### action ###

for d in ['get','post','support']:
   adjustDeploymentDir(
      subdir = d,
      copy = filterfile if d=='get' else copyfile 
   )


### stage and commit the changes ###

dgit.add('-A','.')
dgit.commit(
      '-m',
      'Deploying from ' + source_dir
)



### push to NFS ###

os.chdir(deployment_dir)
os.system('git push nfs master')
   # using system so password verification will work
   # for ssh key verification try
   # dgit.push('nfs','master')

