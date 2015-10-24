import unittest
from FakeSocket import FakeSocket
import tHome as T

#===========================================================================
   
#===========================================================================
class TestVersion ( T.util.test.Case ) :
   def test_version( self ):
      reply = """
53 4D 41 00 00 04 02 A0 00 00
00 01 00 4E 00 10 60 65 13 90
7D 00 AB 94 40 3B 00 A0 F7 00
E0 27 06 72 00 00 00 00 00 00
04 80 01 02 00 58 07 00 00 00
07 00 00 00 01 34 82 00 94 19
AF 53 00 00 00 00 00 00 00 00
FE FF FF FF FE FF FF FF 04 06
60 02 04 06 60 02 00 00 00 00
00 00 00 00 00 00 00 00
"""
      l = T.sma.Link( "fake", connect=False )
      try:
         l.socket = FakeSocket( T.util.hex.toBytes( reply ) )
         o1 = l.version()
   
         l.decode = False
         buf, decoder = l.version()
         o2 = decoder( buf )
      finally:
         l.socket = None
   
      right = T.util.Data(
         version = '02.60.06.R',
         )

      print o1
      
      for k in right.keys():
         r = right[k]
         self.eq( getattr( o1, k ), r, k )
         self.eq( getattr( o2, k ), r, k )

#===========================================================================
