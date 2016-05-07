#!/usr/bin/env python

# dbg-msgHub.py -s "radio" "power/battery"

import argparse
import sys
import pprint
import time
import StringIO
import tHome.util as util
import paho.mqtt.client as mqtt

p = argparse.ArgumentParser( prog=sys.argv[0], 
                             description="Msg Hub debug output" )
p.add_argument( "-p", "--port", type=int, default=1883,
                help="Broker port number to connect to." )
p.add_argument( "-b", "--broker", type=str, default='127.0.0.1',
                help="Broker host name to connect to." )
p.add_argument( "-s", "--skip", nargs="*", default=[] )
c = p.parse_args( sys.argv[1:] )

class Client ( mqtt.Client ):
   def __init__( self ):
      mqtt.Client.__init__( self )
      # Restore callbacks overwritten by stupid mqtt library
      self.on_connect = Client.on_connect
      self.on_message = Client.on_message
      
   def on_connect( self, userData, flags, rc ):
      self.subscribe( '#' )

   def on_message( self, userData, msg ):
      for k in c.skip:
         if msg.topic.startswith( k ):
            return
      
      data = util.json.loads( msg.payload )
      s = StringIO.StringIO()

      t = time.time()
      dt = t - data['time']
      s.write( "dt: %d  " % dt )

      keys = data.keys()
      keys.remove( 'time' )
      for k in sorted( keys ):
         s.write( "%s: %s  " % ( k, data[k] ) )
      
      print "Recv time: %.0f  %-30s %s" % ( t, msg.topic, s.getvalue() )
      #pprint.pprint( data )
      #print data

      
print "Connecting to %s:%d" % ( c.broker, c.port )
client = Client()
client.connect( c.broker, c.port )

# loop_forever() and loop() block ctrl-c signals so it's hard to stop.
# So start in a thread so we can ctrl-c out of this.
client.loop_start()

while True:
   pass

client.loop_stop( force=True )
