#===========================================================================
#
# Error
#
#===========================================================================

""": Stack based error message exception class"""

#===========================================================================
import sys

#===========================================================================
class Error ( Exception ):
   """: Stack based error message exception class.
   """
   
   #-----------------------------------------------------------------------
   @staticmethod
   def raiseException( exception, msg ):
      excType, excValue, trace = sys.exc_info()

      if not isinstance( exception, Error ):
         exception = Error( str( exception ) )

      exception.add( msg )
      
      raise exception, None, trace

   #-----------------------------------------------------------------------
   @staticmethod
   def fromException( exception, msg ):
      excType, excValue, trace = sys.exc_info()

      newError = Error( str( exception ) )
      newError.add( msg )
      
      raise newError, None, trace
      
   #-----------------------------------------------------------------------
   def __init__( self, msg ):
      """: Constructor
      """
      self._msg = [ msg ]
      
      Exception.__init__( self )

   #-----------------------------------------------------------------------
   def add( self, msg ):
      self._msg.append( msg )
      
   #-----------------------------------------------------------------------
   def __str__( self ):
      s = "\n"
      for msg in reversed( self._msg ):
         s += "- %s\n" % msg

      return s
      
   #-----------------------------------------------------------------------

#===========================================================================
