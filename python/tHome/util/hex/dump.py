#===========================================================================
#
# Dump hex bytes to a table.
#
#===========================================================================
import StringIO

#===========================================================================
def dump( buf ):
   """Input is bytes buffer,
   
   Returns a string w/ the hex values in a table
   """
   # Convert to hex characters
   h = [ i.encode( "hex" ).upper() for i in buf ]

   f = StringIO.StringIO()
   f.write( "---: 00 01 02 03 04 05 06 07 08 09\n" )

   for i in range( len( h ) ):
      if i % 10 == 0:
         if i > 0:
            f.write( "\n" )
         f.write( "%03d: " % i )

      f.write( "%2s " % h[i] )

   f.write( "\n" )

   return f.getvalue()

#===========================================================================
