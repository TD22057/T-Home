import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestStatus ( T.util.test.Case ) :
   def test_status( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 4E 00 10 60 65 13 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
08 80 01 02 80 51 00 00 00 00
00 00 00 00 01 48 21 08 82 22
AF 53 23 00 00 00 2F 01 00 00
33 01 00 01 C7 01 00 00 FE FF
FF 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.status()
   
         l.decode = False
         buf, decoder = l.status()
         o2 = decoder( buf )
      finally:
         l.socket = None
   
      right = T.util.Data(
         status = 'Ok',
         )

      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
