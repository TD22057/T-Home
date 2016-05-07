#=============================================================================
#
# JSON utility that turns unicode strings to ascii
#
# NOTE: this file should be named json.py but Python's stupid import
# rules look in the current directory first instead of using absolute
# paths all the time.  So we can't import the global json module if we
# do that.
#
# Code from:
# http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python
#
#=============================================================================
import json

#=============================================================================
# For completeness, add the save API's
dump = json.dump
dumps = json.dumps

#=============================================================================
def load( file ):
   """Same as json.load() but turns unicode to ascii strings.
   """
   return _toStr( json.load( file, object_hook=_toStr ), ignoreDicts=True )

#=============================================================================
def loads( text ):
   """Same as json.loads() but turns unicode to ascii strings.
   """
   return _toStr( json.loads( text, object_hook=_toStr ), ignoreDicts=True )

#=============================================================================
def _toStr( data, ignoreDicts=False ):
   # Convert unicode to string.
   if isinstance( data, unicode ):
      return data.encode( 'utf-8' )
   
   # For lists, process each item.
   if isinstance( data, list ):
      return [ _toStr( i, ignoreDicts=True ) for i in data ]
   
   # For dicts, process keys and values, but only if we haven't
   # already byteified it
   if isinstance( data, dict ) and not ignoreDicts:
      return {
         _toStr( k, ignoreDicts=True ) : _toStr( v, ignoreDicts=True )
         for k, v in data.iteritems()
         }

   # Otherwise return the original object.
   return data

#=============================================================================
