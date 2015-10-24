import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestAcTotalEnergy ( T.util.test.Case ) :
   def test_acTotalEnergy( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 46 00 10 60 65 11 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
0C 80 01 02 00 54 00 00 00 00
01 00 00 00 01 01 26 00 85 22
AF 53 D0 6A 09 00 00 00 00 00
01 22 26 00 82 22 AF 53 2F 3B
00 00 00 00 00 00 00 00 00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.acTotalEnergy()
   
         l.decode = False
         buf, decoder = l.acTotalEnergy()
         o2 = decoder( buf )
      finally:
         l.socket = None
   
      right = T.util.Data(
         totalEnergy = 617168.0,
         dailyEnergy = 15151.0,
         )
      
      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
