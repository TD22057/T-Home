import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestAcPower ( T.util.test.Case ) :
   def test_acPower( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 7A 00 10 60 65 1E 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
10 80 01 02 00 51 07 00 00 00
09 00 00 00 01 40 46 40 86 22
AF 53 B5 07 00 00 B5 07 00 00
B5 07 00 00 B5 07 00 00 01 00
00 00 01 41 46 40 86 22 AF 53
B5 07 00 00 B5 07 00 00 B5 07
00 00 B5 07 00 00 01 00 00 00
01 42 46 40 86 22 AF 53 00 00
00 80 00 00 00 80 00 00 00 80
00 00 00 80 01 00 00 00 00 00
00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.acPower()
   
         l.decode = False
         buf, decoder = l.acPower()
         o2 = decoder( buf )
      finally:
         l.socket = None

      right = T.util.Data(
         acPower1 = 1973.0,
         acPower2 = 1973.0,
         acPower3 = 0.0,
         )
      
      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
