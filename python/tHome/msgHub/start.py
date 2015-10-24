#===========================================================================
#
# Main MsgHub class.
#
#===========================================================================

__doc__ = """Zero-MQ Message Hub

The msgHub is a pub/sub forwarder.  All of the various data producers
send messages to the msgHub as a single point of contact for the
producers.  Consumers of the messages read from the hub as a single
point of contact for the consumers.

Original code from:
http://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/devices/forwarder.html
"""

import zmq
from .. import util

#===========================================================================

def start( inPort, outPort ):
   """Start forwarding messages.

   This function never returns.

   = INPUTS
   - inPort   int: Input XSUB subscriber port number to use.
   - outPort  int: Output XPUB publisher port number to use.
   """
   log = tHome.util.log.get( "msgHub" )

   ctx = zmq.Context()

   intSock, outSock = None, None
   try:
      # Inbound message port.
      log.info( "Starting inbound subscribe socket at port %d" % inPort )
      inSock = ctx.socket( zmq.XSUB )

      # Use * to bind on all interfaces.  Otherwise the address has to
      # be an exact match (127.0.0.1 != IP).
      inSock.bind( "tcp://*:%d" % inPort )

      # Outbound message port.
      log.info( "Starting outbound publish socket at port %d" % outPort )
      outSock = ctx.socket( zmq.XPUB )
      outSock.bind( "tcp://*:%d" % outPort )
      
      # Use ZMP to handle all the forwarding.  We could add logging
      # here but it's easier just to add a new subscriber to read and
      # log any messages.
      #
      # NOTE: this never returns.
      log.info( "Starting forwarding" )
      zmq.device( zmq.FORWARDER, inSock, outSock )

   except ( Exception, KeyboardInterrupt ) as e:
      log.critical( "Exception thrown", exc_info=True )
      raise
      
   finally:
      if inSock:
         inSock.close()

      if outSock:
         outSock.close()

      ctx.term()

#===========================================================================



