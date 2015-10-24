#!/usr/bin/env python

#===========================================================================
#
# Eagle posting server 
#
#===========================================================================

__doc__ = """
"""

import argparse
import bottle as B
import sys
import zmq

import tHome

#===========================================================================
def total( data ):
   msg = {
      "group" : "electric",
      "item" : "total",
      "id" : data.DeviceMacId,
      "label" : "meter",
      "time" : data.TimeUnix,
      "consumed" : data.Consumed, # kWh
      "produced" : data.Produced, # kWh
      }
   
   buf = zmq.utils.jsonapi.dumps( msg )
   zmqSock.send_multipart( [ msg['group'], buf ] )

#===========================================================================
def instant( data ):
   msg = {
      "group" : "electric",
      "item" : "instant",
      "id" : data.DeviceMacId,
      "label" : "meter",
      "time" : data.TimeUnix,
      "power" : data.Power * 1000, # W
      }
   
   buf = zmq.utils.jsonapi.dumps( msg )
   zmqSock.send_multipart( [ msg['group'], buf ] )

#===========================================================================
handlers = {
   #"BlockPriceDetail" : 
   "CurrentSummation" : total,
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
      obj = tHome.eagle.parse( data )
   except:
      log.exception( "Error parsing Eagle posted data" )
      return "ERROR"

   log.info( "Read packet: %s" % obj.name )
   func = handlers.get( obj.name, None )
   if func:
      func( obj )

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

# Parse all the config files and extract the eagle server data.
data = tHome.config.parse( c.configDir )
cfg = tHome.eagle.config.update( data )
hub = tHome.msgHub.config.update( data )

# Override the log file.
if c.log:
   cfg.LogFile = tHome.config.toPath( c.log )

log = tHome.util.log.get( "eagle" )
log.setLevel( cfg.LogLevel )
if cfg.LogFile:
   log.writeTo( cfg.LogFile )

log.info( "Connecting to hub at port %d" % hub.InputPort )
zmqContext = zmq.Context.instance()
zmqSock = zmqContext.socket( zmq.PUB )
zmqSock.connect( "tcp://127.0.0.1:%d" % hub.InputPort )

log.info( "Starting web server at port %d" % cfg.HttpPort )
B.run( host='0.0.0.0', port=cfg.HttpPort, quiet=True )
