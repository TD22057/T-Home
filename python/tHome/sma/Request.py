#===========================================================================
#
# Data request packet
#
#===========================================================================

import logging
import socket
# Import the base header and the struct type codes we're using.
from .Header import *
from .. import util

#===========================================================================
class Data ( Header ):
   _fields = Header._fields + [
      ( uint4, 'command' ),
      ( uint4, 'first' ),
      ( uint4, 'last' ),
      ( uint4, 'trailer' ),
      ]

   struct = util.NamedStruct( 'LITTLE_ENDIAN', _fields )
   
   #------------------------------------------------------------------------
   def __init__( self, command, first, last ):
      Header.__init__( self )

      self.command = command
      self.first = first
      self.last = last
      self.trailer = 0x00

   #------------------------------------------------------------------------
   def send( self, sock ):
      bytes = self.struct.pack( self )

      if self._log.isEnabledFor( logging.DEBUG ):
         self._log.debug( "Send: Request.Data packet\n" + 
                          util.hex.dump( bytes ) )

      # Send the request and read the reply back in.
      try:
         sock.send( bytes )
         reply = sock.recv( 4096 )
         
      except socket.timeout as e:
         msg = "Data request failed - time out error"
         self._log.error( msg )
         util.Error.raiseException( e, msg )
         
      if self._log.isEnabledFor( logging.DEBUG ):
         self._log.debug( "Recv: Reply packet\n" + util.hex.dump( reply ) )
      
      return reply

   #------------------------------------------------------------------------

#===========================================================================
