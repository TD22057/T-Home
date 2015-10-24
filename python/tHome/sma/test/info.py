import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestInfo ( T.util.test.Case ) :
   def test_info( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 C6 00 10 60 65 31 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
05 80 01 02 00 58 00 00 00 00
03 00 00 00 01 1E 82 10 82 19
AF 53 53 4E 3A 20 31 39 31 33
30 30 36 30 34 38 00 00 10 00
00 00 10 00 00 00 00 00 00 00
00 00 00 00 01 1F 82 08 82 19
AF 53 41 1F 00 01 42 1F 00 00
FE FF FF 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00
00 00 00 00 01 20 82 08 82 19
AF 53 EE 23 00 00 EF 23 00 00
F0 23 00 00 F1 23 00 01 F2 23
00 00 F3 23 00 00 F4 23 00 00
F5 23 00 00 01 20 82 08 82 19
AF 53 FE FF FF 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
"""
      l = T.sma.Link( "fake", connect=False, raw=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.info()
   
         l.decode = False
         buf, decoder = l.info()
         o2 = decoder( buf )
      finally:
         l.socket = None
   
      right = T.util.Data(
         name = 'SN: 1913006048',
         model = 'SB 5000TLUS-22',
         type = 'Solar Inverter',
         )

      print o1

      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
