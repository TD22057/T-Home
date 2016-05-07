#===========================================================================
#
# Acurite bridge parser
#
#===========================================================================
import argparse
import json
import sys
from .. import broker
from . import config
from .decode import decode
from . import mqtt


#===========================================================================
def process( config, text, sensorMap ):
   idx = text.find( "id=" )
   if idx == -1:
      return []

   # Parse the data from the HTTP command.
   data = decode( text[idx:], sensorMap )
   if not data:
      return []

   # Convert to a list of MQTT  (topic, payload) tuples.
   return mqtt.convert( config, data )

#===========================================================================
def run( args, input=sys.stdin ):
   """DEPRECATED

   This function is used when intercepting bridge traffic.  The new
   way redirects bridge traffic which bin/tHome-acurite.py handles so
   this function isn't needed any more.
   """
   
   p = argparse.ArgumentParser( prog=args[0], 
                                description="Acurite decoder" )
   p.add_argument( "-c", "--configDir", metavar="configDir",
                   default="/var/config/tHome",
                   help="T-Home configuration directory." )
   p.add_argument( "-l", "--log", metavar="logFile",
                   default=None, help="Logging file to use.  Input 'stdout' "
                   "to log to the screen." )
   c = p.parse_args( args[1:] )
   
   # Parse the acurite config file.
   cfg = config.parse( c.configDir )
   log = config.log( cfg, c.log )

   sensorMap = {}
   for s in cfg.sensors:
      sensorMap[s.id] = s
   
   # Create the MQTT client and connect it to the broker.
   client = broker.connect( c.configDir, log )

   while True:
      line = sys.stdin.readline()
      msgs = process( cfg, line, sensorMap )

      for topic, data in msgs:
         log.info( "Publish: %s: %s" % ( topic, payload ) )
         payload = json.dumps( data )
         client.publish( topic, payload )
      
#===========================================================================
