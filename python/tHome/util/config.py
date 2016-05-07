#===========================================================================
#
# Config file utilities.
#
#===========================================================================

__doc__ = """Config file utilities.
"""

from . import path
from . import fimport

#===========================================================================
class Entry:
   def __init__( self, name, cvt, default=None ):
      self.name = name
      self.cvt = cvt
      self.default = default
      
#===========================================================================
def readAndCheck( configDir, configFile, entries ):
   # Combine the dir and file, expand any variables, and read the
   # python code into a module.
   configPath = path.expand( configDir, configFile )
   m = fimport.fimport( configPath )

   # Check the input values for the correc types and assign any
   # default values.
   check( m, entries )
   return m

#===========================================================================
def check( input, entries ):
   if isinstance( input, dict ):
      checkDict( input, entries )
      return
   
   # Use the sections to do error checking.
   for e in entries:
      if not hasattr( input, e.name ):
         value = e.default
         
      # Run the converter function on the input.  This validates the
      # input type and can do any other manipulations it wants.
      elif e.cvt:
         inputValue = getattr( input, e.name )
         value = e.cvt( inputValue )
         
      setattr( input, e.name, value )
      
#===========================================================================
def checkDict( input, entries ):
   assert( isinstance( input, dict ) )
   
   # Use the sections to do error checking.
   for e in entries:
      if not e.name in input:
         value = e.default
         
      # Run the converter function on the input.  This validates the
      # input type and can do any other manipulations it wants.
      elif e.cvt:
         inputValue = input[e.name]
         value = e.cvt( inputValue )
         
      input[e.name] = value
      
#===========================================================================
