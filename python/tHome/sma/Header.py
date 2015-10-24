#===========================================================================
#
# Common data packet structures.  Used for requests and replies.
#
#===========================================================================
from .. import util

#===========================================================================

# Struct type codes
uint1 = "B"
uint2 = "H"
uint4 = "I"
uint8 = "Q"
int1 = "b"
int2 = "h"
int4 = "i"
int8 = "q"

#==============================================================================
class Header:
   _fields = [
      # Header fields
      ( uint4, 'hdrMagic' ),
      ( uint4, 'hdrUnknown1' ),
      ( uint4, 'hdrUnknown2' ),
      ( uint1, 'packetHi' ),     # packet length in little endian hi word
      ( uint1, 'packetLo' ),     # packet length in little endian low word
      ( uint4, 'signature' ),
      ( uint1, 'wordLen' ),      # int( packetLen / 4 )
      ( uint1, 'hdrUnknown3' ),
      # Common packet fields
      ( uint2, 'destId', ),
      ( uint4, 'destSerial', ),
      ( uint2, 'destCtrl', ),
      ( uint2, 'srcId', ),
      ( uint4, 'srcSerial', ),
      ( uint2, 'srcCtrl', ),
      ( uint2, 'error', ),
      ( uint2, 'fragmentId', ),
      ( uint1, 'packetId', ),
      ( uint1, 'baseUnknown', ),
      ]
      
   _hdrSize = 20 # bytes for the header fields.
   _nextPacketId = 0

   #------------------------------------------------------------------------
   def __init__( self ):
      assert( self.struct )
      
      self.hdrMagic = 0x00414D53
      self.hdrUnknown1 = 0xA0020400
      self.hdrUnknown2 = 0x01000000
      self.signature = 0x65601000
      self.hdrUnknown3 = 0xA0

      # NOTE: self.struct must be created by the derived class.  That
      # allows this to compute the correct packet length and encode it.
      packetLen = len( self.struct ) - self._hdrSize
      self.packetHi = ( packetLen >> 8 ) & 0xFF
      self.packetLo = packetLen & 0xFF
      self.wordLen = int( packetLen / 4 )
       
      # Any destination - we send to a specific IP address so this
      # isn't important.
      self.destId = 0xFFFF 
      self.destSerial = 0xFFFFFFFF
      self.destCtrl = 0x00
      self.srcId = 0x7d # TODO change this?
      self.srcSerial = 0x334657B0 # TODO change this?
      self.srcCtrl = 0x00
      self.error = 0
      self.fragmentId = 0
      self.baseUnknown = 0x80

      # Packet id is 1 byte so roll over at 256.
      self._nextPacketId += 1
      if self._nextPacketId == 256:
         self._nextPacketId = 1

      self.packetId = self._nextPacketId

      self._log = util.log.get( "sma" )

   #------------------------------------------------------------------------
   def bytes( self ):
      return self.struct.pack( self )

   #------------------------------------------------------------------------

#===========================================================================
