#===========================================================================
#
# Log on/off packets
#
#===========================================================================

import logging
import socket
import time
# Import the base header and the struct type codes we're using.
from .Header import *
from .. import util

#===========================================================================
class LogOn ( Header ):
   _fields = Header._fields + [
      ( uint4, 'command' ),
      ( uint4, 'group' ),
      ( uint4, 'timeout' ),
      ( uint4, 'time' ),
      ( uint4, 'unknown1' ),
      ( '12s', "password" ),
      ( uint4, 'trailer' ),
      ]

   struct = util.NamedStruct( 'LITTLE_ENDIAN', _fields )
   
   #------------------------------------------------------------------------
   def __init__( self, group, password ):
      assert( len( password ) <= 12 )
      assert( group == "USER" or group == "INSTALLER" )

      Header.__init__( self )

      if group == "USER":
         self.group = 0x00000007
         passOffset = 0x88
      else: # installer
         self.group = 0x0000000A
         passOffset = 0xBB
      
      self.password = ""

      # Loop over each character and encode it as hex and offset by
      # the group code offset.
      for i in range( 12 ):
         if i < len( password ):
            c = int( password[i].encode( 'hex' ), 16 ) + passOffset

         # Pad out to 12 bytes w/ the group code offset.
         else:
            c = passOffset

         # Turn the hex code back to a character.
         self.password += chr( c )

      self.destCtrl = 0x0100
      self.srcCtrl = 0x0100
      
      self.command = 0xFFFD040C
      self.timeout = 0x00000384 # 900 sec
      self.time = int( time.time() )
      self.unknown1 = 0x00
      self.trailer = 0x00

   #------------------------------------------------------------------------
   def send( self, sock ):
      # Pack ourselves into the message structure.
      bytes = self.struct.pack( self )

      if self._log.isEnabledFor( logging.DEBUG ):
         self._log.debug( "Send: LogOn packet\n" + util.hex.dump( bytes ) )

      try:
         # Send the message and receive the response back.
         sock.send( bytes )
         bytes = sock.recv( 4096 )
         
      except socket.timeout as e:
         msg = "Can't log on - time out error"
         self._log.error( msg )
         util.Error.raiseException( e, msg )

      if self._log.isEnabledFor( logging.DEBUG ):
         self._log.debug( "Recv: LogOn reply\n" + util.hex.dump( bytes ) )

      # Overwrite our fields w/ the reply data.
      self.struct.unpack( self, bytes )
      if self.error:
         raise util.Error( "Error trying to log on to the SMA inverter.  "
                           "Group/password failed." )
      
   #------------------------------------------------------------------------

#===========================================================================
class LogOff ( Header ):
   _fields = Header._fields + [
      ( uint4, 'command' ),
      ( uint4, 'unknown1' ),
      ( uint4, 'trailer' ),
      ]

   struct = util.NamedStruct( 'LITTLE_ENDIAN', _fields )

   #------------------------------------------------------------------------
   def __init__( self ):
      Header.__init__( self )

      self.destCtrl = 0x0300
      self.srcCtrl = 0x0300

      self.command = 0xFFFD010E
      self.unknown1 = 0xFFFFFFFF
      self.trailer = 0x00

   #------------------------------------------------------------------------
   def send( self, sock ):
      bytes = self.struct.pack( self )

      if self._log.isEnabledFor( logging.DEBUG ):
         self._log.debug( "Send: LogOff packet\n" + util.hex.dump( bytes ) )
      
      sock.send( bytes )

   #------------------------------------------------------------------------

#===========================================================================
