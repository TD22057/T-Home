#===========================================================================
#
# Thermostat class
#
#===========================================================================

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
   def __init__( self, label, ipAddress, room=None ):
      self.label = label
      self.ip = ipAddress
      self.room = room if room is not None else label

      self._log = util.log.get( "thermostat" )
      self._lastStatus = None

   #------------------------------------------------------------------------
   def status( self ):
      self._log.info( "%s:%s Getting status" % ( self.ip, self.label ) )
      
      url = "http://%s/tstat" % self.ip
      r = requests.get( url )

      self._log.info( "%s:%s Received status %s" % ( self.ip, self.label,
                                                     r.status_code ) )
      if r.status_code != requests.codes.ok:
         self._lastStatus = None
         e = util.Error( r.text )
         e.add( "Error requesting status from the thermostat '%s' at %s" %
                ( self.label, self.ip ) )
         raise e

      d = r.json()

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
         override = bool( d["override"] ),
         hold = bool( d["hold"] ),
         )

      if "t_heat" in d:
         m.target = d["t_heat"]
      else:
         m.target = d["t_cool"]
         
      self._log.info( "%s:%s Received: %s" % ( self.ip, self.label, m ) )
      
      self._lastStatus = m
      return m
       
   #------------------------------------------------------------------------
   def messages( self, data=None ):
      data = data if data is not None else self._lastStatus
      if not data:
         return []

      s = self._lastStatus
      msgs = [
         {
            "group" : "weather",
            "item" : "temperature",
            "label" : self.room,
            "time" : s.time,
            "temperature" : s.temperature,
            },
         {
            "group" : "hvac",
            "item" : "thermostat",
            "label" : self.label,
            "time" : s.time,
            "target" : s.target,
            "temperature" : s.temperature,
            "fanMode" : s.fanMode,
            "fanState" : s.fanState,
            "tempMode" : s.tempMode,
            "tempState" : s.tempState,
            "override" : s.override,
            "hold" : s.hold,
            },
         ]
         
      return msgs
   
   #------------------------------------------------------------------------
   def __str__( self ):
      return """Thermostat(
   Label = '%s',
   IP = '%s',
   )""" % ( self.label, self.ip )
   
   #------------------------------------------------------------------------
