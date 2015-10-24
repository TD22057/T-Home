#===========================================================================
#
# Convert a hex string to bytes
#
#===========================================================================
import math

#===========================================================================
def toBytes( hexStr ):
   """Input is a string containing hex values (w/ or w/o spaces)

   Return is the same value in a bytes array.
   """
   s = hexStr.strip().replace( "\n", " " )
   s = ''.join( s.split(" ") )

   bytes = []
   for i in range( 0, len( s ), 2 ):
      bytes.append( chr( int( s[i:i+2], 16 ) ) )

   return ''.join( bytes )
 
#===========================================================================
