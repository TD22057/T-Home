#===========================================================================
#
# Main report processing
#
#===========================================================================

import astral
import calendar
import datetime
import time
import zmq
from .. import util
from . import report

_debug = False

#===========================================================================
def start( config, hubConfig ):
   fromts = datetime.datetime.fromtimestamp

   log = util.log.get( "sma" )

   linkArgs = { "ip" : config.IP,  "port" : config.Port, 
                "group" : config.Group, "password" : config.Password, }

   addr = "%s:%d" % ( hubConfig.Host, hubConfig.InputPort )
   log.info( "Connecting to hub at %s" % addr )
   zmqContext = zmq.Context.instance()
   zmqSock = zmqContext.socket( zmq.PUB )
   zmqSock.connect( "tcp://%s" % ( addr ) )
   
   reports = []
   if config.PollFull > 0:
      reports.append( util.Data( lbl="full", func=msgFull,
                                 poll=config.PollFullpollFull, nextT=0 ) )

   if config.PollEnergy > 0:
      reports.append( util.Data( lbl="energy", func=msgEnergy,
                                 poll=config.PollEnergy, nextT=0 ) )

   if config.PollPower > 0:
      reports.append( util.Data( lbl="power", func=msgPower,
                                 poll=config.PollPower, nextT=0 ) )

   if not reports:
      log.error( "No reports specified, all poll times <= 0" )
      return
   
   t0 = time.time()

   useRiseSet = ( config.Lat is not None and config.Lon is not None )

   log.info( "Startup time    : %s" % fromts( t0 ) )
   if useRiseSet:
      timeRise = sunRise( config.Lat, config.Lon )
      timeSet = sunSet( config.Lat, config.Lon )
      log.info( "Today's sun rise: %s" % fromts( timeRise ) )
      log.info( "Today's sun set : %s" % fromts( timeSet ) )
   else:
      timeRise = 0
      timeSet = 3e9 # jan, 2065

   # Current time is before todays sun rise.  Start reporting at the
   # rise time and stop reporting at the set time.
   if t0 < timeRise:
      timeBeg = timeRise - config.TimePad
      timeEnd = timeSet + config.TimePad
      log.info( "Before sun rise, sleeping until %s" % fromts( timeBeg ) )
      
   # Current time is after todays sun set.  Start reporting at
   # tomorrows rise time and stop reporting at tomorrows set time.
   elif t0 > timeSet:
      timeBeg = sunRise( config.Lat, config.Lon, +1 ) - config.TimePad
      timeEnd = sunSet( config.Lat, config.Lon, +1 ) + config.TimePad
      log.info( "After sun set, sleeping until %s" % fromts( timeBeg ) )

   # Current time is between todays rise and set.  Start reporting
   # immediately and stop reporting at the set time.
   else:
      timeBeg = t0
      timeEnd = timeSet + config.TimePad
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
         nextReport.func( zmqSock, linkArgs, config.Label, log )
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
            reports[0].func( zmqSock, linkArgs, config.Label, log )
         
         timeBeg = sunRise( config.Lat, config.Lon, +1 ) - config.TimePad
         timeEnd = sunSet( config.Lat, config.Lon, +1 ) + config.TimePad
         _initTimes( reports, timeBeg )
         
         log.info( "After sun set, sleeping until %s" % fromts( timeBeg ) )
                   

#===========================================================================
def _initTimes( reports, timeBeg ):
   # Set the first time to be the begin time + the polling interval.
   for r in reports:
      r.nextT = timeBeg + r.poll

   # Run the biggest priority report once right at startup.  
   reports[0].nextT = timeBeg
      
#===========================================================================
def msgPower( zmqSock, linkArgs, label, log ):
   if not _debug:
      data = report.power( **linkArgs )
   else:
      data = { 'time' : 1, 'timeOff' : 2, 'dcPower' : 3, 'acPower' : 4 }
      
   msg = _buildPowerMsg( data, label, log )
   
   buf = zmq.utils.jsonapi.dumps( msg )
   zmqSock.send_multipart( [ msg['group'], buf ] )

#===========================================================================
def msgEnergy( zmqSock, linkArgs, label, log ):
   if not _debug:
      data = report.energy( **linkArgs )
   else:
      data = { 'time' : 1, 'timeOff' : 2, 'dcPower' : 3, 'acPower' : 4,
               'dailyEnergy' : 5, 'totalEnergy' : 6 }
      
   msgs = [
      _buildPowerMsg( data, label, log ),
      _buildEnergyMsg( data, label, log ),
      ]

   for m in msgs:
      buf = zmq.utils.jsonapi.dumps( m )
      zmqSock.send_multipart( [ m['group'], buf ] )

#===========================================================================
def msgFull( zmqSock, linkArgs, label, log ):
   if not _debug:
      data = report.full( **linkArgs )
   else:
      data = { 'time' : 1, 'timeOff' : 2, 'dcPower' : 3, 'acPower' : 4,
               'dailyEnergy' : 5, 'totalEnergy' : 6, 'foo' : 7, 'bar' : 8 }
   
   msgs = [
      _buildPowerMsg( data, label, log ),
      _buildEnergyMsg( data, label, log ),
      _buildFullMsg( data, label, log ),
      ]

   for m in msgs:
      buf = zmq.utils.jsonapi.dumps( m )
      zmqSock.send_multipart( [ m['group'], buf ] )
   
#===========================================================================
def _buildPowerMsg( data, label, log ):
   msg = {
      "group" : "solar",
      "item" : "power",
      "label" : label,
      "time" : data["time"],
      "timeOff" : data["timeOff"],
      "acPower" : data["acPower"],
      "dcPower" : data["dcPower"],
      }

   log.info( "%(label)s AC power: %(acPower)s W", msg )
   return msg

#===========================================================================
def _buildEnergyMsg( data, label, log ):
   msg = {
      "group" : "solar",
      "item" : "energy",
      "label" : label,
      "time" : data["time"],
      "timeOff" : data["timeOff"],
      "dailyEnergy" : data["dailyEnergy"],
      "totalEnergy" : data["totalEnergy"],
      }

   log.info( "%(label)s Daily energy: %(dailyEnergy)s kWh", msg )
   return msg

#===========================================================================
def _buildFullMsg( data, label, log ):
   msg = {
      "group" : "solar",
      "item" : "full",
      "label" : "label",
      }
   msg.update( data.__dict__ )
   return msg

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
