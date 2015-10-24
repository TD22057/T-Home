import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestTemp ( T.util.test.Case ) :
   def test_temp( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 42 00 10 60 65 10 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
09 80 01 02 00 52 00 00 00 00
00 00 00 00 01 77 23 40 44 22
AF 53 AC 1B 00 00 B6 1B 00 00
B2 1B 00 00 B2 1B 00 00 01 00
00 00 00 00 00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.temperature()
   
         l.decode = False
         buf, decoder = l.temperature()
         o2 = decoder( buf )
      finally:
         l.socket = None
   
      right = T.util.Data(
         temperature = 70.84,
         )

      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
