import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestGridFrequency ( T.util.test.Case ) :
   def test_gridFrequency( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 42 00 10 60 65 10 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
13 80 01 02 00 51 13 00 00 00
13 00 00 00 01 57 46 00 86 22
AF 53 6C 17 00 00 6C 17 00 00
6C 17 00 00 6C 17 00 00 01 00
00 00 00 00 00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.gridFrequency()
   
         l.decode = False
         buf, decoder = l.gridFrequency()
         o2 = decoder( buf )
      finally:
         l.socket = None
   
      right = T.util.Data(
         frequency = 59.96,
         )

      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
