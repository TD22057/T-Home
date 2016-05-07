#!/usr/bin/env python

#===========================================================================
#
# Eagle posting server 
#
#===========================================================================

__doc__ = """
Starts a small web server to read packets sent from an Acurite Bridgek.

The Acurite must be redirected to post messages to server instead of
it's main server.  This assumes the Bridge is connected to a raspberry
pi using a USB network adaptor with it's network bridged to the main
network.  NOTE: The last port number in the iptables command must
match the port configured in conf/acurite.py for the acurite web
server.

ebtables -t broute -A BROUTING -p IPv4 --ip-protocol 6 --ip-destination-port 80 -j redirect --redirect-target ACCEPT
iptables -t nat -A PREROUTING -i br0 -p tcp --dport 80 -j REDIRECT --to-port 22041

Scripts uses the tHome.acurite package to decode the bridge posts and
converts them to JSON dictionaries which get sent out as MQTT
messages.
"""

import argparse
import bottle as B
import sys
import json
import tHome as T

#===========================================================================
@B.post( '/' )
@B.post( '/messages/' )
def bridge_post():
   content = B.request.body.read( B.request.content_length )
   
   log.info( "Read: %s" % content )

   # Convert the line to messages.  Returns a list of tuples of
   # ( topic, dict ).
   msgs = T.acurite.cmdLine.process( cfg, content, sensorMap )

   # Send the messages out.
   for topic, data in msgs:
      log.info( "Publish: %s: %s" % ( topic, data ) )

      payload = json.dumps( data )
      client.publish( topic, payload )

   # Standard acurite web site reply - found by watching traffic to
   # the acurite web site.
   return { "success" : 1, "checkversion" : "126" }

#===========================================================================
#
# Main applications script
#
#===========================================================================

p = argparse.ArgumentParser( prog=sys.argv[0],
                             description="T-Home Acurite Server" )
p.add_argument( "-c", "--configDir", metavar="configDir",
                default="/etc/tHome",
                help="Configuration file directory." )
p.add_argument( "-l", "--log", metavar="logFile",
                default=None, help="Logging file to use.  Input 'stdout' "
                "to log to the screen." )
c = p.parse_args( sys.argv[1:] )

# Parse the eagle config file.
cfg = T.acurite.config.parse( c.configDir )
log = T.acurite.config.log( cfg, c.log )

# Create a sensor map from the configuration file.
sensorMap = {}
for s in cfg.sensors:
   sensorMap[s.id] = s

# Create the MQTT client and connect it to the broker.
client = T.broker.connect( c.configDir, log )

# Start the MQTT as a background thread. This way we can run the web
# server as the main thread here.
client.loop_start()

log.info( "Starting web server at port %d" % cfg.httpPort )
B.run( host='0.0.0.0', port=cfg.httpPort, quiet=True )

