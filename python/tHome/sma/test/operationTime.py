import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestOperationTime ( T.util.test.Case ) :
   def test_OperationTime( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 46 00 10 60 65 11 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
0D 80 01 02 00 54 03 00 00 00
04 00 00 00 01 2E 46 00 85 22
AF 53 00 FA 0E 00 00 00 00 00
01 2F 46 00 85 22 AF 53 42 97
0E 00 00 00 00 00 00 00 00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.operationTime()
   
         l.decode = False
         buf, decoder = l.operationTime()
         o2 = decoder( buf )
      finally:
         l.socket = None
   
      right = T.util.Data(
         operationTime = 981504.0,
         feedTime = 956226.0,
         )

      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
