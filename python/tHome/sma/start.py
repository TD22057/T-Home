#===========================================================================
#
# Main report processing
#
#===========================================================================

import astral
import calendar
import datetime
import json
import time
from .. import util
from . import report

#===========================================================================
def start( config, client, debug=False ):
   fromts = datetime.datetime.fromtimestamp

   log = util.log.get( "sma" )

   linkArgs = { "ip" : config.host,  "port" : config.port, 
                "group" : config.group, "password" : config.password, }

   reports = []
   if config.pollFull > 0:
      reports.append( util.Data( lbl="full", func=msgFull,
                                 poll=config.pollFull, nextT=0 ) )

   if config.pollEnergy > 0:
      reports.append( util.Data( lbl="energy", func=msgEnergy,
                                 poll=config.pollEnergy, nextT=0 ) )

   if config.pollPower > 0:
      reports.append( util.Data( lbl="power", func=msgPower,
                                 poll=config.pollPower, nextT=0 ) )

   if not reports:
      log.error( "No reports specified, all poll times <= 0" )
      return
   
   t0 = time.time()

   useRiseSet = ( config.lat is not None and config.lon is not None )

   log.info( "Startup time    : %s" % fromts( t0 ) )
   if useRiseSet:
      timeRise = sunRise( config.lat, config.lon )
      timeSet = sunSet( config.lat, config.lon )
      log.info( "Today's sun rise: %s" % fromts( timeRise ) )
      log.info( "Today's sun set : %s" % fromts( timeSet ) )
   else:
      timeRise = 0
      timeSet = 3e9 # jan, 2065

   # Current time is before todays sun rise.  Start reporting at the
   # rise time and stop reporting at the set time.
   if t0 < timeRise:
      timeBeg = timeRise - config.timePad
      timeEnd = timeSet + config.timePad
      log.info( "Before sun rise, sleeping until %s" % fromts( timeBeg ) )
      
   # Current time is after todays sun set.  Start reporting at
   # tomorrows rise time and stop reporting at tomorrows set time.
   elif t0 > timeSet:
      timeBeg = sunRise( config.lat, config.lon, +1 ) - config.timePad
      timeEnd = sunSet( config.lat, config.lon, +1 ) + config.timePad
      log.info( "After sun set, sleeping until %s" % fromts( timeBeg ) )

   # Current time is between todays rise and set.  Start reporting
   # immediately and stop reporting at the set time.
   else:
      timeBeg = t0
      timeEnd = timeSet + config.timePad
      log.info( "Sun up, run until sunset %s" % fromts( timeEnd ) )
      
   _initTimes( reports, timeBeg )

   while True:
      nextReport = min( reports, key=lambda x: x.nextT )

      dt = nextReport.nextT - t0
      if dt > 0:
         log.info( "Sleeping %s sec for report %s" % ( dt, nextReport.lbl ) )
         time.sleep( dt )

      log.info( "Running report : %s" % nextReport.lbl )
      try:
         nextReport.func( client, linkArgs, config, log )
      except:
         log.exception( "Report failed to run" )
         
      nextReport.nextT += nextReport.poll
      
      t0 = time.time()

      # Time is now after the end time for today.
      if t0 > timeEnd:
         # If the last report wasn't the largest one, run the largest
         # report one last time.  This gives us a final tally of
         # energy production for example.
         if nextReport != reports[0]:
            reports[0].func( client, linkArgs, config, log )
         
         timeBeg = sunRise( config.lat, config.lon, +1 ) - config.timePad
         timeEnd = sunSet( config.lat, config.lon, +1 ) + config.timePad
         _initTimes( reports, timeBeg )
         
         log.info( "After sun set, sleeping until %s" % fromts( timeBeg ) )
                   

#===========================================================================
def sunRise( lat, lon, dayOffset=0 ):
   t = datetime.date.today() + datetime.timedelta( days=dayOffset )

   a = astral.Astral()
   utc = a.sunrise_utc( t, lat, lon )

   # Convert the UTC datetime to a UNIX time stamp.
   return calendar.timegm( utc.timetuple() )
   
#===========================================================================
def sunSet( lat, lon, dayOffset=0 ):
   t = datetime.date.today() + datetime.timedelta( days=dayOffset )

   a = astral.Astral()
   utc = a.sunset_utc( t, lat, lon )

   # Convert the UTC datetime to a UNIX time stamp.
   return calendar.timegm( utc.timetuple() )
   
#===========================================================================
def msgPower( client, linkArgs, config, log ):
   data = report.power( **linkArgs )
   msg = _buildPowerMsg( data, log )

   payload = json.dumps( msg )
   
   log.info( "Publish: %s: %s" % ( config.mqttPower, payload ) )
   client.publish( config.mqttPower, payload )

#===========================================================================
def msgEnergy( client, linkArgs, config, log ):
   data = report.energy( **linkArgs )

   msgs = [
      # ( topic name, msg dict )
      ( config.mqttPower, _buildPowerMsg( data, log ) ),
      ( config.mqttEnergy, _buildEnergyMsg( data, log ) ),
      ]

   for topic, data in msgs:
      payload = json.dumps( data )

      log.info( "Publish: %s: %s" % ( topic, payload ) )
      client.publish( topic, payload )

#===========================================================================
def msgFull( client, linkArgs, config, log ):
   data = report.full( **linkArgs )
   
   msgs = [
      # ( topic name, msg dict )
      ( config.mqttPower, _buildPowerMsg( data, log ) ),
      ( config.mqttEnergy, _buildEnergyMsg( data, log ) ),
      ( config.mqttFull, _buildFullMsg( data, log ) ),
      ]
   
   for topic, data in msgs:
      payload = json.dumps( data )
      client.publish( topic, payload )
   
#===========================================================================
def _buildPowerMsg( data, log ):
   msg = {
      "time" : data["time"],
      "acPower" : data["acPower"], # in W
      "dcPower" : data["dcPower"], # in W
      }

   log.info( "AC power: %(acPower)s W", msg )
   return msg

#===========================================================================
def _buildEnergyMsg( data, log ):
   msg = {
      "time" : data["time"],
      "dailyEnergy" : data["dailyEnergy"] / 1000.0, # Wh -> kWh
      "totalEnergy" : data["totalEnergy"] / 1000.0, # Wh -> kWh
      }

   log.info( "Daily energy: %(dailyEnergy)s kWh", msg )
   return msg

#===========================================================================
def _buildFullMsg( data, log ):
   return data.__dict__

#===========================================================================
def _initTimes( reports, timeBeg ):
   # Set the first time to be the begin time + the polling interval.
   for r in reports:
      r.nextT = timeBeg + r.poll

   # Run the biggest priority report once right at startup.  
   reports[0].nextT = timeBeg
      
#===========================================================================
