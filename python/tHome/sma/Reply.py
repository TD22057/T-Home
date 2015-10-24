#===========================================================================
#
# Data reply packets
#
#===========================================================================

import struct
from .. import util
# Import the base header and the struct type codes we're using.
from .Header import *
from . import tags

#===========================================================================

class Value ( Header, util.Data ):
   _fields = Header._fields + [
      ( uint4, 'command' ),
      ( uint4, 'first' ),
      ( uint4, 'last' ),
      ]

   struct = util.NamedStruct( 'LITTLE_ENDIAN', _fields )
   
   def __init__( self, decoders ):
      self.values = []
      self._decoders = decoders
      Header.__init__( self )
      util.Data.__init__( self )

   def __call__( self, bytes, raw=False, obj=None ):
      return self.decode( bytes, raw, obj )
   
   def decode( self, bytes, raw=False, obj=None ):
      # Unpack the base data.
      self.struct.unpack( self, bytes )

      offset = len( self.struct )
      for d in self._decoders:
         offset += d.decodeItem( self, bytes, offset )

      if raw:
         return self

      r = obj if obj is not None else util.Data()
      for item in self.values:
         for varFrom, varTo in item._variables:
            value = getattr( item, varFrom )
            setattr( r, varTo, value )

      return r

#==============================================================================
class BaseItem ( util.Data ):
   _fields = [
      ( uint1, 'mppNum' ),
      ( uint2, 'msgType' ),
      ( uint1, 'dataType' ),
      ( uint4, 'time' ),
      ]

   _baseSize = 8 # bytes

   def __init__( self, var, size, timeVar=None ):
      self.variable = var
      self._size = size

      self._variables = []
      if timeVar:
         self._variables.append( ( 'time', timeVar ) )
         
      util.Data.__init__( self )

   def decodeBase( self, obj, attrVal ):
      setattr( obj, self.variable, attrVal )
      obj.values.append( self )
      
      return self._size

#==============================================================================
class StringItem ( BaseItem ):
   def __init__( self, var, size, timeVar=None ):
      BaseItem.__init__( self, var, size, timeVar )

      self._fields = BaseItem._fields + [
         ( '%ds' % ( size - BaseItem._baseSize ), "bytes" ),
         ]
      self._struct = util.NamedStruct( 'LITTLE_ENDIAN', self._fields )

      self._variables.append( ( 'value', var ) )

   def decodeItem( self, obj, bytes, offset ):
      self._struct.unpack( self, bytes, offset )

      s = self.bytes
      idx = s.find( "\0" )
      if idx != -1:
         s = s[:idx]

      self.value = s
      
      return BaseItem.decodeBase( self, obj, self.value )
      
   
#==============================================================================
class AttrItem ( BaseItem ):
   struct = util.NamedStruct( 'LITTLE_ENDIAN', BaseItem._fields )
   
   def __init__( self, var, size, timeVar=None ):
      BaseItem.__init__( self, var, size, timeVar )

      self._numAttr = ( size - BaseItem._baseSize ) / 4
      self._variables.append( ( 'value', var ) )

   def decodeItem( self, obj, bytes, offset ):
      self.struct.unpack( self, bytes, offset )
      offset += len( self.struct )

      # Little endian, 4 individual unsigned bytes
      s = struct.Struct( '<BBBB' )

      for i in range( self._numAttr ):
         # x[0], x[1], x[2] are the attribute code
         # x[3] == 1 if the attribute is active or 0 if not
         # Only 1 active attribute per block
         x = s.unpack_from( bytes, offset )
         if x[3] == 1:
            self.code = x[2]*65536 + x[1]*256 + x[0]
            self.value = tags.values.get( self.code, "Unknown" )
            break
         
         offset += s.size
         
      return BaseItem.decodeBase( self, obj, self.value )
   
#==============================================================================
class BaseInt ( BaseItem ):
   def __init__( self, var, size, mult=1.0, timeVar=None ):
      BaseItem.__init__( self, var, size, timeVar )
      self._mult = mult
      self._variables.append( ( 'value', var ) )
      
   def decodeItem( self, obj, bytes, offset ):
      self.struct.unpack( self, bytes, offset )
      
      if self.value == self.nan:
         self.value = 0
      else:
         self.value *= self._mult
         
      return BaseItem.decodeBase( self, obj, self.value )
   
#==============================================================================
class I32Item ( BaseInt ):
   _fields = BaseInt._fields + [
      ( int4, 'value' ),
      ]

   struct = util.NamedStruct( 'LITTLE_ENDIAN', _fields )
   nan = -0x80000000 # SMA int32 NAN value
   
#==============================================================================
class U32Item ( BaseInt ):
   _fields = BaseInt._fields + [
      ( uint4, 'value' ),
      ]

   struct = util.NamedStruct( 'LITTLE_ENDIAN', _fields )
   nan = 0xFFFFFFFF # SMA uint32 NAN value
   
#==============================================================================
class I64Item ( BaseInt ):
   _fields = BaseInt._fields + [
      ( int8, 'value' ),
      ]

   struct = util.NamedStruct( 'LITTLE_ENDIAN', _fields )
   nan = -0x8000000000000000 # SMA int64 NAN value
   
#==============================================================================
class U64Item ( BaseInt ):
   _fields = BaseInt._fields + [
      ( uint8, 'value' ),
      ]

   struct = util.NamedStruct( 'LITTLE_ENDIAN', _fields )

   def __init__( self, size, var, mult=1.0 ):
      # 0xFFFFFFFFFFFFFFFF == SMA uint64 NAN value
      BaseInt.__init__( self, 0xFFFFFFFFFFFFFFFF, size, var, mult )
   
#==============================================================================
class VersionItem ( BaseItem ):
   _fields = BaseItem._fields + [
      ( uint4, 'value' ),
      ( uint4, 'value2' ),
      ( uint4, 'value3' ),
      ( uint4, 'value4' ),
      ( uint1, 'verType' ),
      ( uint1, 'verBuild' ),
      ( uint1, 'verMinor' ),
      ( uint1, 'verMajor' ),
      ]

   struct = util.NamedStruct( 'LITTLE_ENDIAN', _fields )
   
   def __init__( self, var ):
      BaseItem.__init__( self, var, 24 )
      self._variables.append( ( 'version', var ) )

   def decodeItem( self, obj, bytes, offset ):
      self.struct.unpack( self, bytes, offset )

      if self.verType > 5:
         relType = str( self.verType )
      else:
         relType = "NEABRS"[self.verType]

      self.version = '%02x.%02x.%02x.%s' % ( self.verMajor, self.verMinor,
                                             self.verBuild, relType )

      return BaseItem.decodeBase( self, obj, self.version )
      
   
#==============================================================================
   
