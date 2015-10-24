#!/usr/bin/env python

import argparse
import zmq
import sys
import pprint
import time

p = argparse.ArgumentParser( prog=sys.argv[0], 
                             description="Msg Hub debug output" )
p.add_argument( "-b", "--brief", action="store_true",
                help="One line brief output." )
p.add_argument( "-p", "--port", type=int, default=22041,
                help="Msg Hub port number to connect to." )
p.add_argument( "-g", "--group", type=str, default="",
                help="Message group to read." )
p.add_argument( "-s", "--strings", type=str, nargs="*", default=[],
                help="String to match." )
c = p.parse_args( sys.argv[1:] )

ctx = zmq.Context()
s = ctx.socket( zmq.SUB )
s.setsockopt( zmq.SUBSCRIBE, c.group )
s.connect( "tcp://127.0.0.1:%d" % c.port )

def temp( x ):
   if x["label"] == "Unknown":
      return None
   
   h = x.get( 'humidity', -1 )
   if h == -1:
      return "t=%s" % ( x['temperature'] )
   else:
      return "t=%s h=%s" % ( x['temperature'], h )
   
valueMap = {
   "electric.instant" : lambda x: "power=%s" % x['power'],
   "electric.total" : lambda x: "c=%s p=%s" % ( x['consumed'], x['produced'] ),
   "weather.temperature" : temp,
   "weather.rain" : lambda x: "rain=%s" % x['rainfall'],
   "weather.wind" : lambda x: "wind=%s at %s" % ( x['speed'], x['direction'] ),
   "weather.pressure" : lambda x: "pressure=%s" % ( x['pressure'] ),
   "hvac.thermostat" : lambda x: "mode=%s temp=%s vs %s" %
                       ( x['tempState'], x['temperature'], x['target'] ),
   "solar.power" : lambda x: "ac=%s W" % x["acPower"],
   "solar.energy" : lambda x: "total=%s kWh" % ( x["dailyEnergy"]*1e-3 ),
   }

def defaultPrint( data ):
   print "Unknown: %s.%s" % ( data['group'], data['item'] )
   pprint.pprint( data )

while True:
   group, buf = s.recv_multipart()
   t = time.time()
   
   data = zmq.utils.jsonapi.loads( buf )
   if not c.brief:
      print "====="
      print "Recv Time:",t
      pprint.pprint( data )
      continue

   
   l = "%s.%s" % ( data['group'], data['item'] )
   func = valueMap.get( l, defaultPrint )

   out = func( data )
   if out is None:
      defaultPrint( data )
      continue
      
   show = True
      
   if c.strings:
      show = False
      for pat in c.strings:
         if pat in out:
            show = True
            break
         
   if not show:
      continue
   
   print "%.3f %s %s %s %s" % ( data['time'], data['group'],
                                data['item'], data['label'], out )

