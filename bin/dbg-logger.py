#!/usr/bin/env python

import argparse
import zmq
import os
import sys
import pprint
import time

p = argparse.ArgumentParser( prog=sys.argv[0], 
                             description="Msg Hub debug output" )
p.add_argument( "-d", "--debug", action="store_true",
                help="Print debug messages to the screen." )
p.add_argument( "outputDir", type=str, 
                help="Output directory to save data to." )
c = p.parse_args( sys.argv[1:] )

ctx = zmq.Context()
s = ctx.socket( zmq.SUB )
s.setsockopt( zmq.SUBSCRIBE, '' )
s.connect( "tcp://127.0.0.1:22041" )

def temp( x ):
   h = x.get( 'humidity', -1 )
   if h == -1:
      return "%s" % ( x['temperature'] )
   else:
      return "%s,%s" % ( x['temperature'], h )
   
valueMap = {
   "electric.instant" : lambda x: x['power'],
   "electric.total" : lambda x: "%s,%s" % ( x['consumed'], x['produced'] ),
   "weather.temperature" : temp,
   "weather.rain" : lambda x: x['rainfall'],
   "weather.wind" : lambda x: "%s,%s" % ( x['speed'], x['direction'] ),
   "weather.pressure" : lambda x: "%s" % ( x['pressure'] ),
   "hvac.thermostat" : lambda x: "%s,%s,%s" %
                       ( x['tempState'], x['temperature'], x['target'] ),
   "solar.power" : lambda x: "%s" % x["acPower"],
   "solar.energy" : lambda x: "%s" % ( x["dailyEnergy"]*1e-3 ),
   }

if not os.path.exists( c.outputDir ):
   os.mkdir( c.outputDir )

files = {}

try:
   while True:
      group, buf = s.recv_multipart()
      data = zmq.utils.jsonapi.loads( buf )
   
      fname = "%s_%s_%s.csv" % ( data['group'], data['item'], data['label'] )
   
      if fname not in files:
         p = os.path.join( c.outputDir, fname )
         files[fname] = open( p, "a" )
   
      f = files[fname]
      
      if data['label'] == "Unknown":
         value = str( data )
      else:
         l = "%s.%s" % ( data['group'], data['item'] )
         value = valueMap[l]( data )
   
      if c.debug:
         print "%0.1f %-40s = %s" % ( data['time'], fname, value )
            
      print >> f, "%s,%s" % ( data['time'], value )
      f.flush()

finally:
   for f in files.itervalues():
      f.close()
      
         
   
