#===========================================================================
#
# Thermostat class
#
#===========================================================================

import json
import requests
import time
from .. import util 

#===========================================================================
class Thermostat:
   # Temperature mode
   tmode = { 0 : "off", 1 : "heat", 2 : "cool", 3 : "auto" }
   # Active heating/cooling flag.
   tstate = { 0 : "off", 1 : "heat", 2 : "cool" }

   # Fan mode
   fmode = { 0 : "auto", 1 : "circulate", 2 : "on" }
   # Fan on/off flag.
   fstate = { 0 : "off", 1 : "on" }
   
   #------------------------------------------------------------------------
   def __init__( self, label, host, mqttTempTopic, mqttModeTopic,
                 mqttStateTopic, mqttSetTopic ):
      self.label = label
      self.host = host
      self.mqttTempTopic = mqttTempTopic
      self.mqttModeTopic = mqttModeTopic
      self.mqttStateTopic = mqttStateTopic
      self.mqttSetTopic = mqttSetTopic

      self._log = util.log.get( "thermostat" )
      self._lastStatus = None

      
   #------------------------------------------------------------------------
   def status( self ):
      self._log.info( "%s:%s Getting status" % ( self.host, self.label ) )
      
      url = "http://%s/tstat" % self.host
      r = requests.get( url )

      self._log.info( "%s:%s Received status %s" % ( self.host, self.label,
                                                     r.status_code ) )
      if r.status_code != requests.codes.ok:
         self._lastStatus = None
         e = util.Error( r.text )
         e.add( "Error requesting status from the thermostat '%s' at %s" %
                ( self.label, self.host ) )
         raise e

      d = r.json()

      tempControl = 'auto'
      if d["override"]:
         tempControl = 'override'
      elif d['hold']:
         tempControl = 'hold'

      m = util.Data(
         # Unix time.
         time = time.time(),
         # Current temperature at thermostat.
         temperature = d["temp"],
         # Thermostat mode (off, heating, cooling
         tempMode = self.tmode[ d["tmode" ] ],
         # Is the hvac currently running?
         tempState = self.tstate[ d["tstate" ] ],
         # Fan mode (auto, on)
         fanMode = self.fmode[ d["fmode" ] ],
         # Is the fan current on?
         fanState = self.fstate[ d["fstate" ] ],
         # program or override mode
         tempControl = tempControl,
         )

      if "t_heat" in d:
         m.target = d["t_heat"]
      else:
         m.target = d["t_cool"]
         
      self._log.info( "%s:%s Received: %s" % ( self.host, self.label, m ) )
      
      self._lastStatus = m
      return m
       
   #------------------------------------------------------------------------
   def messages( self, data=None ):
      data = data if data is not None else self._lastStatus
      if not data:
         return []

      s = self._lastStatus
      msgs = [
         # tuple of ( topic, message )
         ( self.mqttTempTopic, {
            'time' : s.time,
            'temp' : s.temperature,
            } ),
         ( self.mqttModeTopic, {
            'time' : s.time,
            'sys' : s.tempMode,
            'fan' : s.fanMode,
            'temp' : s.tempControl,
            } ),
         ( self.mqttStateTopic, {
            'time' : s.time,
            'active' : s.tempState,
            'fan' : s.fanState,
            'target' : s.target,
            'temp' : s.temperature,
            } ),
         ]
         
      return msgs
   
   #------------------------------------------------------------------------
   def processSet( self, client, msg ):
      data = json.loads( msg.payload )
      replyTopic = msg.topic + "/" + data['id']

      status = None
      if '/temp' in msg.topic:
         value = data['temp']
         # TODO: set temperature
         status = 0
         msg = ""
      elif '/mode' in msg.topic:
         sysMode = data['sys'] # off/heat/cool/auto
         fanMode = data['fan'] # on/auto
         # TODO: set mode
         status = 0
         msg = ""

      if status is not None:
         reply = { time : time.time(), error : status, msg : msg }
         payload = json.dumps( reply )
         client.publish( replyTopic, payload )
   
   #------------------------------------------------------------------------
   def __str__( self ):
      return """Thermostat(
   Label = '%s',
   Host = '%s',
   )""" % ( self.label, self.host )
   
   #------------------------------------------------------------------------
