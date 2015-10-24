#=============================================================================
#
# Testing utilites.
#
#=============================================================================

import unittest

#=============================================================================
class Case( unittest.TestCase ):
   def __init__( self, cls ):
      unittest.TestCase.__init__( self, cls )
      
   def setup( self ):
      pass

   def teardown( self ):
      pass
   
   def eq( self, a, b, msg=None ):
      if not a == b:
         msg = msg if msg else ""
         #self._errors.append( "%s %r != %r" % ( msg, a, b ) )
         self.fail( "%s %r != %r" % ( msg, a, b ) )

   def neq( self, a, b, msg=None ):
      if not a != b:
         msg = msg if msg else ""
         #self._errors.append( "%s %r == %r" % ( msg, a, b ) )
         self.fail( "%s %r == %r" % ( msg, a, b ) )
