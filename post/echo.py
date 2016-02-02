def respond( env, req_obj, send_response ):
     send_response(
         "<h1>Your message was:</h1><p>" +
         req_obj.payload.upper()
         "</p>"
     ) 

