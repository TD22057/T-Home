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
