pappy - PortAudio Pushed to PYthon
----------------------------------
Dale Cieslak <dsizzle@github>

pappy is a pretty simple wrapping of the PortAudio library using Pyrex.  I didn't make any attempts to make it "Pythonic" in that there are no Python classes or constructs; it's simply a 1-for-1 mapping to the C library.  I've tried to keep most of the function calls identical to the C version wherever possible.  

NOTE: pappy REQUIRES PortAudio to be installed in order to run.  This should be obvious, but I'm pointing it out just in case it's not.  

NOTE: Pyrex (http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/) is required to build pappy.  It's a bit old so someday I might switch to Cython...but Pyrex works really well for now.

NOTE: Only tested with 32-bit Python.

See the api_info.txt file for API specifics.


