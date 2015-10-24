#===========================================================================
#
# Config parsing
#
#===========================================================================

__doc__ = """Config parsing.
"""

from .util import Data
import ConfigParser
import glob
import os.path

#===========================================================================
def parse( configDir ):
   # Parse the files.  Default xform makes all keys lower case so set
   # it to str to stop that behavior.
   p = ConfigParser.ConfigParser()
   p.optionxform = str

   files = glob.glob( os.path.join( configDir, "*.conf" ) )
   for f in files:
      p.read( f )

   cfg = Data( _config = p )
   for s in p.sections():
      d = Data()
      for o in p.options( s ):
         setattr( d, o, p.get( s, o ) )

      setattr( cfg, s, d )

   return cfg

#===========================================================================
def update( data, secDef ):
   for section, fields in secDef.iteritems():
      if not hasattr( data, section ):
         setattr( data, section, Data() )

      secData = data[section]
      for name, convertFunc, defaultValue in fields:
         if hasattr( secData, name ):
            secData[name] = convertFunc( secData[name] )

         else:
            secData[name] = defaultValue

#===========================================================================
def toPath( value ):
   """TODO: doc
   """
   if value is None:
      return None
   
   value = str( value )
   
   if "$" in value:
      value = os.path.expandvars( value )
      
   if "~" in value:
      value = os.path.expanduser( value )

   return value

#===========================================================================
