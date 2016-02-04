def respond( env, req_obj, send_response ):
     print "ECHOING"
     send_response(
         "ok",
         "<h1>Your message was:</h1><p>" +
         req_obj.payload.upper() +
         "</p>"
     ) 

