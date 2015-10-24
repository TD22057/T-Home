import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestAcTotalPower ( T.util.test.Case ) :
   def test_acTotalPower( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 42 00 10 60 65 10 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
12 80 01 02 00 51 00 00 00 00
00 00 00 00 01 3F 26 40 86 22
AF 53 6A 0F 00 00 6A 0F 00 00
6A 0F 00 00 6A 0F 00 00 01 00
00 00 00 00 00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.acTotalPower()
   
         l.decode = False
         buf, decoder = l.acTotalPower()
         o2 = decoder( buf )
      finally:
         l.socket = None
   
      right = T.util.Data(
         acPower = 3946.0,
         )
      
      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
