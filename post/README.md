The `post` Subdir
----------------

This is the root of the directory of your those Python files which
exchange objects with Javascript in the browser, that is to say the
"responding" Python files.

If your Javascript does `json_out` to send an object to a
`rel_path`, then `rel_path` is relative to this directory and
determines the Python file which will get the object (with `jsonIn`)
and respond to it (with `jsonOut`).

If
you run `serveYOS.py` from the `install` subdir these are the Python files
that will be found.  

If you run an `install...` program from that directory, these are the 
responding Python
files that will be installed.

Do not place helper Python files in this directory.
