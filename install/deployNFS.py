#! /usr/local/bin/python

with open('deployCommon.py') as fi:
   exec( fi.read() )

### action ###

for d in ['get','post','py']:
   adjustDeploymentDir(
      source_dir = source_dir,
      target_dir = deployment_dir,
      subdir = 'get',
      files = getFiles(source_dir, 'get'),
      copy = filterfile if d=='get' else copyfile 
   )


### stage and commit the changes ###

dgit.add('-A','.')
dgit.commit(
      '-m',
      'Deploying\n\n   ' +
         '\n   '.join(cur_deployment)
)



### push to NFS ###

os.system('git push nfs master')
   # using system so password verification will work
   # for ssh key verification try
   # dgit.push('nfs','master')

