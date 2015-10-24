import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestDcPower ( T.util.test.Case ) :
   def test_dcPower( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 5E 00 10 60 65 17 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
0E 80 01 02 80 53 00 00 00 00
01 00 00 00 01 1E 25 40 85 22
AF 53 13 08 00 00 13 08 00 00
13 08 00 00 13 08 00 00 01 00
00 00 02 1E 25 40 85 22 AF 53
21 08 00 00 21 08 00 00 21 08
00 00 21 08 00 00 01 00 00 00
00 00 00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.dcPower()
   
         l.decode = False
         buf, decoder = l.dcPower()
         o2 = decoder( buf )
      finally:
         l.socket = None

      right = T.util.Data(
         dcPower1 = 2067.0,
         dcPower2 = 2081.0,
         )
      
      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
