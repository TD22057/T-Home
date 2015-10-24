import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestAcVoltage ( T.util.test.Case ) :
   def test_acVoltage( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 01 22 00 10 60 65 48 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
11 80 01 02 00 51 0A 00 00 00
12 00 00 00 01 48 46 00 86 22
AF 53 A6 2F 00 00 A6 2F 00 00
A6 2F 00 00 A6 2F 00 00 01 00
00 00 01 49 46 00 86 22 AF 53
9B 2F 00 00 9B 2F 00 00 9B 2F
00 00 9B 2F 00 00 01 00 00 00
01 4A 46 00 86 22 AF 53 FF FF
FF FF FF FF FF FF FF FF FF FF
FF FF FF FF 01 00 00 00 01 4B
46 00 86 22 AF 53 43 5F 00 00
43 5F 00 00 43 5F 00 00 43 5F
00 00 01 00 00 00 01 4C 46 00
86 22 AF 53 FF FF FF FF FF FF
FF FF FF FF FF FF FF FF FF FF
01 00 00 00 01 4D 46 00 86 22
AF 53 FF FF FF FF FF FF FF FF
FF FF FF FF FF FF FF FF 01 00
00 00 01 50 46 00 86 22 AF 53
35 3F 00 00 35 3F 00 00 35 3F
00 00 35 3F 00 00 01 00 00 00
01 51 46 00 86 22 AF 53 35 3F
00 00 35 3F 00 00 35 3F 00 00
35 3F 00 00 01 00 00 00 01 52
46 00 86 22 AF 53 FF FF FF FF
FF FF FF FF FF FF FF FF FF FF
FF FF 01 00 00 00 00 00 00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.acVoltage()
   
         l.decode = False
         buf, decoder = l.acVoltage()
         o2 = decoder( buf )
      finally:
         l.socket = None

      right = T.util.Data(
         acVoltage1 = 121.98,
         acVoltage2 = 121.87,
         acVoltage3 = 0,
         acGridVoltage = 243.87,
         unknown1 = 0,
         unknown2 = 0,
         acCurrent1 = 16.181,
         acCurrent2 = 16.181,
         acCurrent3 = 0,
         )
      
      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
