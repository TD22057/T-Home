#===========================================================================
#
# Base class for messages
#
#===========================================================================
import datetime
from . import convert

#==========================================================================
class Base:
   def __init__( self, name, node=None ):
      self.name = name

      # Copy the attributes.
      if node is not None:
         for child in node:
            setattr( self, child.tag, child.text )

      # Convert hex values to int and float.
      convert.hexKeys( self, self._numHexKeys, float )
      convert.hexKeys( self, self._intHexKeys, int )

   #------------------------------------------------------------------------
   def msgDict( self ):
      assert( self._jsonKeys )

      msg = {}
      for key in self._jsonKeys:
         if hasattr( self, key ):
            msg[key] = getattr( self, key )
            
      if hasattr( self, "TimeUnix" ):
         msg["Time"] = self.TimeUnix

      return msg
      
      
   #------------------------------------------------------------------------
   def _format( self, indent=3 ):
      i = " "*indent
      s = "%s(\n" % self.name

      for key in dir( self ):
         if key[0] == "_":
            continue
         
         v = getattr( self, key )
         if callable( v ):
            continue

         if hasattr( v, "_format" ):
            s += "%s%s : %s,\n" % ( i, key, v._format( indent+3 ) )
         elif isinstance( v, str ):
            s += "%s%s : '%s',\n" % ( i, key, v )
         else:
            s += "%s%s : %s,\n" % ( i, key, v )

      s += "%s)" % i
      return s
      
   #------------------------------------------------------------------------
   def __str__( self ):
      return self._format()
      
   def __repr__( self ):
      return self.__str__()

   #------------------------------------------------------------------------
   
#==========================================================================
