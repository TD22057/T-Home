#!/usr/bin/env python

#===========================================================================
#
# Radio thermostats reader
#
#===========================================================================

import argparse
import sys
import time
import zmq
import tHome

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

# Parse all the config files and extract the eagle server data.
data = tHome.config.parse( c.configDir )
therm = tHome.thermostat.config.update( data )
hub = tHome.msgHub.config.update( data )

# Override the log file.
if c.log:
   therm.LogFile = tHome.config.toPath( c.log )

log = tHome.util.log.get( "thermostat" )
log.setLevel( therm.LogLevel )
if therm.LogFile:
   log.writeTo( therm.LogFile )

addr = "%s:%d" % ( hub.Host, hub.InputPort )
log.info( "Connecting to hub at %s" % addr )
zmqContext = zmq.Context.instance()
zmqSock = zmqContext.socket( zmq.PUB )
zmqSock.connect( "tcp://%s" % ( addr ) )

while True:
   t0 = time.time()
   for t in therm.thermostats:
      try:
         t.status()
         msgs = t.messages()
         for m in msgs:
            buf = zmq.utils.jsonapi.dumps( m )
            zmqSock.send_multipart( [ m['group'], buf ] )
         
      except:
         log.exception( "Error getting thermostat status." )

   dt = time.time() - t0
   delay = max( therm.PollTime, therm.PollTime-dt )
   time.sleep( delay )
         

