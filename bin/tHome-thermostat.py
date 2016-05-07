#!/usr/bin/env python

#===========================================================================
#
# Radio thermostats reader
#
#===========================================================================

import argparse
import sys
import time
import json
import tHome as T

#===========================================================================

#===========================================================================
#
# Main applications script
#
#===========================================================================

p = argparse.ArgumentParser( prog=sys.argv[0],
                             description="T-Home Thermostats" )
p.add_argument( "-c", "--configDir", metavar="configDir",
                default="/etc/tHome",
                help="Configuration file directory." )
p.add_argument( "-l", "--log", metavar="logFile",
                default=None, help="Logging file to use.  Input 'stdout' "
                "to log to the screen." )
c = p.parse_args( sys.argv[1:] )

# Parse the thermostat config file.
cfg = T.thermostat.config.parse( c.configDir )
log = T.thermostat.config.log( cfg, c.log )

# Create the MQTT client and connect it to the broker.
client = T.broker.connect( c.configDir, log )

# Handle set messages being set to the thermostats.
def on_message( client, userData, msg ):
   for t in cfg.thermostats:
      if mqtt.topic_matches_sub( t.mqttSetTopic, msg.topic ):
         t.processSet( client, msg )
         return

client.on_message = on_message

# Subscribe to the set messages.
for t in cfg.thermostats:
   print t
   client.subscribe( t.mqttSetTopic )

# Start the MQTT as a background thread. This way we can run the web
# server as the main thread here.
client.loop_start()

while True:
   t0 = time.time()
   for t in cfg.thermostats:
      try:
         # Poll the thermostat for status.
         t.status()

         # Publish any messages.
         msgs = t.messages()
         for topic, msg in msgs:
            payload = json.dumps( msg )
            client.publish( topic, payload )
         
      except Exception as e:
         # This prints a stack trace which is more than we really want.
         #log.exception( "Error getting thermostat status." )
         log.error( "Error getting thermostat status: " + str( e ) )

   dt = time.time() - t0
   delay = max( cfg.pollTime, cfg.pollTime-dt )
   time.sleep( delay )
         

