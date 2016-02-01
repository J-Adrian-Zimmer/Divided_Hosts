Divided Hosts
=====================

This repo is being developed for the forthcoming "Single Page
Apps on Divided Hosts".
 
A single page application divides an application's work up by 
putting more of it on the user's computer and less on the server.  Such an app is started
with the loading of one
page.  Javascript in that page then interacts with the user and the server,
morphing the page as necessary. The resulting application
can require less network traffic and enable more efficient servers than a traditional application.  

"Divided Hosts" means that the single page and other static material
is placed on one server and the dynamic server responders are placed
on a second server.  Each server can be optimized for what it does.

As with traditional applications, a database
engine is typically included on a private network with the server
or, perhaps, on the same machine as the server.

Hence "Single Page Apps on Divided Hosts" describes deployments on
two hosts in which one host serves files and the other responds to
requests from the browser.   Both hosts exist in the cloud and can
be scaled up as necessary.   In our version browser and server communicate by sending objects back and forth as in this diagram

```
Browser   <-->   Python Server   <-->   Mongo Database
          AJAX                 Pymongo
        (jQuery)             
```

Those of us who build relatively small and low volume applications like to 
work entirely on our own computers.  Hence the
need for a development process that lets us create on one machine and then
deploy to the cloud. 

Although scaling applications is easy on such hosts as Firebase, Heroku, and Openshift,
a flourshing small application is likely to consume more
resources than is available without charge on those servers. For such an application the inexpensive approach may be to give everything to the NearlyFreeSpeech host.

"Single Page Apps on Divided Hosts" explains how to build
applications that can be deployed interchangeably among 
these platforms

> **YOS**`   `Your Own Server  (static and dynamic)

> **NFS**`   `NearlyFreeSpeech  (static and dynamic)

> **FH**`   `Firebase (static) + Heroku (dynamic)

> **FA**`   `Firebase (static) + Openshift (dynamic)

Python 2.7.x has been chosen to run the dynamic serving, also to run
the server on YOS.  The Mongo 3.2.x  as a supportive database. 

This repo will contain progressively sophisticated examples.  If you want to follow the development of this repo 
check back now and then.   If you have the time and ability to look at, and make constructive comments about, "Single Page Apps on Divided Hosts" as it is being written, then contact me through the email address at [my web site](http://www.jazimmer.net).  When everything is finished this ReadMe will change accordingly.

