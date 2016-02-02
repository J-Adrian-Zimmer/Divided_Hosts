def addFromItems(table,p):
   return (
     table + ("<tr><td>%s</td><td>%s</td></tr>" % p)
   )

def respond( env, req_obj, send_response ):
      from project_runpy import env2
      send_response( 
         
         'ok',
         
         "<h1>Using <code>wsgi's env parameter</code></h1><table>" +
         reduce(addFromItems, env.items(),[]) +
         "</table>" +

         "<h1>Using <code>project_runpy</code></h1><table>" + 
         reduce(addFromItems, env2.items(),[]) +
         "</table>" +

      )
