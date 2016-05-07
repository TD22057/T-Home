#===========================================================================
#
# Broker connection
#
#===========================================================================
from . import config
import paho.mqtt.client as mqtt

#===========================================================================
class Client( mqtt.Client ):
   """Logging client
   """
   def __init__( self, log=None ):
      mqtt.Client.__init__( self )
      self._logger = log
      # Restore callbacks overwritten by stupid mqtt library
      self.on_log = Client.on_log
      
   def on_log( self, userData, level, buf ):
      if self._logger:
         self._logger.log( level, buf )

#===========================================================================
def connect( configDir, log, client=None ):
   cfg = config.parse( configDir )

   if client is None:
      client = Client( log )

   if cfg.user:
      client.username_pw_set( cfg.user, cfg.password )

   if cfg.ca_certs:
      client.tls_set( cfg.ca_certs, cfg.certFile, cfg.keyFile )

   log.info( "Connecting to broker at %s:%d" % ( cfg.host, cfg.port ) )
   client.connect( cfg.host, cfg.port, cfg.keepAlive )

   return client

#===========================================================================



