import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestAcMaxPower ( T.util.test.Case ) :
   def test_acMaxPower( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 7A 00 10 60 65 1E 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
0B 80 01 02 00 51 01 00 00 00
03 00 00 00 01 1E 41 00 82 22
AF 53 88 13 00 00 88 13 00 00
88 13 00 00 88 13 00 00 01 00
00 00 01 1F 41 00 82 22 AF 53
88 13 00 00 88 13 00 00 00 00
00 00 88 13 00 00 00 00 00 00
01 20 41 00 82 22 AF 53 88 13
00 00 88 13 00 00 00 00 00 00
88 13 00 00 00 00 00 00 00 00
00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.acMaxPower()
   
         l.decode = False
         buf, decoder = l.acMaxPower()
         o2 = decoder( buf )
      finally:
         l.socket = None

      right = T.util.Data(
         acMaxPower1 = 5000.0,
         acMaxPower2 = 5000.0,
         acMaxPower3 = 5000.0,
         )
      
      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
