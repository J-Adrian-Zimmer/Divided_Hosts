def respond( env2, req_obj, send_response ):
   from project_runpy import env
   
   def addFromItems(table,p):
      return (
        table + ("<tr><td>%s</td><td>%s</td></tr>" % p)
      )

   try:
      content = (
       "<h1>Using <code>wsgi's env parameter</code></h1>" +
       "<table border=1 rules='all' frame='box'>" +
       reduce(addFromItems, env2.items(),'') +
       "</table>" +

       "<h1>Using <code>project_runpy</code></h1>" +
       "<table border=1 rules='all' frame='box'>" +
       reduce(addFromItems, env.items(),'') +
       "</table>"
      )
      send_response( 'ok', content )
   except Exception as e:
      send_response(
         'error',
         'ERROR: ' + str(e)
      ) 

