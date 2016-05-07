#!/usr/bin/env python

#===========================================================================
#
# Eagle posting server 
#
#===========================================================================

__doc__ = """
Starts a small web server.  The Rain Forest Eagle is configured with
this web server as it's 'cloud' provider so it posts messages to the
server as XML data packets.

Scripts uses the tHome.eagle package to decode the XML packets and
converts them to JSON dictionaries which get sent out as MQTT
messages.
"""

import argparse
import bottle as B
import sys
import json
import tHome as T

#===========================================================================
def meter( client, data, cfg ):
   msg = {
      "time" : data.TimeUnix,
      "consumed" : data.Consumed, # kWh
      "produced" : data.Produced, # kWh
      }

   return ( cfg.mqttEnergy, msg )

#===========================================================================
def instant( client, data, cfg ):
   msg = {
      "time" : data.TimeUnix,
      "power" : data.Power * 1000, # W
      }

   return ( cfg.mqttPower, msg )
   
#===========================================================================
handlers = {
   #"BlockPriceDetail" : 
   "CurrentSummation" : meter,
   #"DeviceInfo" : 
   #"FastPollStatus" : 
   "InstantaneousDemand" : instant,
   #"MessageCluster" : 
   #"MeterInfo" : 
   #"NetworkInfo" : 
   #"PriceCluster" : 
   #"Reading" : 
   #"ScheduleInfo" :
   #"TimeCluster" : 
   }

#===========================================================================

@B.post( '/' )
def root_post():
   data = B.request.body.read( B.request.content_length )
   try:
      obj = T.eagle.parse( data )
   except:
      log.exception( "Error parsing Eagle posted data" )
      return "ERROR"

   log.info( "Read packet: %s" % obj.name )
   
   func = handlers.get( obj.name, None )
   if func:
      topic, msg = func( client, obj, cfg )
      if msg:
         log.info( "Publish: %s: %s" % ( topic, msg ) )
         
         payload = json.dumps( msg )
         client.publish( topic, payload )

   return "ok"

#===========================================================================
#
# Main applications script
#
#===========================================================================

p = argparse.ArgumentParser( prog=sys.argv[0],
                             description="T-Home Eagle Server" )
p.add_argument( "-c", "--configDir", metavar="configDir",
                default="/etc/tHome",
                help="Configuration file directory." )
p.add_argument( "-l", "--log", metavar="logFile",
                default=None, help="Logging file to use.  Input 'stdout' "
                "to log to the screen." )
c = p.parse_args( sys.argv[1:] )

# Parse the eagle config file.
cfg = T.eagle.config.parse( c.configDir )
log = T.eagle.config.log( cfg, c.log )

# Create the MQTT client and connect it to the broker.
client = T.broker.connect( c.configDir, log )

# Start the MQTT as a background thread. This way we can run the web
# server as the main thread here.
client.loop_start()

log.info( "Starting web server at port %d" % cfg.httpPort )
B.run( host='0.0.0.0', port=cfg.httpPort, quiet=True )
