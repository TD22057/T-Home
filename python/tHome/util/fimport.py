#===========================================================================
#
# Arbitrary file importing utility.  Does NOT modify sys.modules
#
#===========================================================================
import imp
import os

def fimport( filePath ):
   # Read the file and compile the code.  This will fail if the file
   # doesn't exist or there are problems w/ the syntax in the file.
   with open( filePath, 'r' ) as f:
      code = compile( f.read(), filePath, "exec", dont_inherit=True )

   # Get the absolute path and the file name w/o the directory or
   # extension to set into the module variables.
   absPath = os.path.abspath( filePath )
   d, fileName = os.path.split( filePath )
   rootName, ext = os.path.splitext( fileName )

   # Create a new module and exec the code in it's context.  
   m = imp.new_module( rootName )
   m.__file__ = absPath
   exec code in m.__dict__

   # Return the module object.
   return m

