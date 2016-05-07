#===========================================================================
#
# File and directory utilities.
#
#===========================================================================

import os
import os.path
from .Error import Error

#===========================================================================
def makeDirs( fileName ):
   """TODO: docs
   """
   try:
      d = os.path.dirname( fileName )
      if d and not os.path.exists( d ):
         os.makedirs( d )

   except ( IOError, OSError ) as e:
      msg = "Error trying to create intermediate directories for the file: " \
            "'%s'" % ( fileName )
      Error.raiseException( e, msg )
      
#===========================================================================
def expand( filePath, fileName=None ):
   """Combine a directory and file name and expand env variables and ~.

   A full path can be input in filePath.  Or a directory can be input
   in filePath and a file name input in fileName.
   """
   if fileName:
      filePath = os.path.join( filePath, fileName )
      
   filePath = str( filePath )
   if "$" in filePath:
      filePath = os.path.expandvars( filePath )
      
   if "~" in filePath:
      filePath = os.path.expanduser( filePath )

   return filePath
   
#===========================================================================
