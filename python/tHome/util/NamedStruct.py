#===========================================================================
#
# Named structure field class
#
#===========================================================================
import struct
from .Data import Data

#==============================================================================
class NamedStruct:

   #---------------------------------------------------------------------------
   def __init__( self, endian, elems ):
      """Constructr
      
      endian == BIG_ENDIAN or LITTLE_ENDIAN
      elems = [ ( struct_format_code, name ), ... ]
      """
      assert( endian == "BIG_ENDIAN" or endian == "LITTLE_ENDIAN" )
      
      if endian == "BIG_ENDIAN":
         self.format = ">"
      elif endian == "LITTLE_ENDIAN":
         self.format = "<"

      self.format += "".join( [ i[0] for i in elems ] )
      self.names = [ i[1] for i in elems ]

      self.struct = struct.Struct( self.format )

   #---------------------------------------------------------------------------
   def __len__( self ):
      return self.struct.size

   #---------------------------------------------------------------------------
   def pack( self, obj ):
      data = [ getattr( obj, i ) for i in self.names ]
      return self.struct.pack( *data )

   #---------------------------------------------------------------------------
   def unpack( self, obj, bytes, offset=0 ):
      if obj is None:
         obj = Data()

      data = self.struct.unpack_from( bytes, offset )
      for i in range( len( self.names ) ):
         setattr( obj, self.names[i], data[i] )

      return obj

#==============================================================================
