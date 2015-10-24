import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestDcVoltage ( T.util.test.Case ) :
   def test_dcVoltage( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 96 00 10 60 65 25 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
0F 80 01 02 80 53 02 00 00 00
05 00 00 00 01 1F 45 40 85 22
AF 53 B1 5E 00 00 B1 5E 00 00
B1 5E 00 00 B1 5E 00 00 01 00
00 00 02 1F 45 40 85 22 AF 53
D5 5E 00 00 D5 5E 00 00 D5 5E
00 00 D5 5E 00 00 01 00 00 00
01 21 45 40 85 22 AF 53 51 21
00 00 51 21 00 00 51 21 00 00
51 21 00 00 01 00 00 00 02 21
45 40 85 22 AF 53 7D 21 00 00
7D 21 00 00 7D 21 00 00 7D 21
00 00 01 00 00 00 00 00 00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.dcVoltage()
   
         l.decode = False
         buf, decoder = l.dcVoltage()
         o2 = decoder( buf )
      finally:
         l.socket = None

      right = T.util.Data(
         dcVoltage1 = 242.41,
         dcVoltage2 = 242.77,
         dcCurrent1 = 8.529,
         dcCurrent2 = 8.573,
         )
      
      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
