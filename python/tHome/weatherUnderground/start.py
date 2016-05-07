#===========================================================================
#
# Main report processing
#
#===========================================================================

import logging
import requests
import datetime
import threading
import numpy as np
import time
from StringIO import StringIO
from .. import util

#===========================================================================
class CircularTimeBuf:
   """Circular buffer class.

   This stores data in a numpy array as a circular buffer that covers
   a set amount of time.  When data is added (with a time tag), it
   will automatically erase any data older than the input time length.
   This allows for fast and easy computations involving the last n
   seconds of data regardless of the rate that data is seen.
   """
   def __init__( self, timeLen, maxRate, label=None, log=None ):
      self.label = label if label is not None else ""
      self.log = log
      
      numEntries = int( timeLen / maxRate )

      self._dt = timeLen
      self._len = numEntries

      # Index of the last entry added to the buffer.  -1 is used to
      # indicate that no data is present.
      self._lastIdx = -1

      # Create an array of NaN values. v[0] is the array of times,
      # v[1] is the array of values.
      self.v = np.full( ( 2, self._len ), np.nan )

   #--------------------------------------------------------------------------
   def __nonzero__( self ):
      return self._lastIdx != -1
      
   #--------------------------------------------------------------------------
   def append( self, t, v ):
      # Remove any data older than t-self._dt
      self.updateTo( t )

      idx = self._nextIdx( self._lastIdx )

      self.v[0][idx] = t
      self.v[1][idx] = v

      self._lastIdx = idx

      # Debugging output
      if self.log and self.log.isEnabledFor( logging.DEBUG ):
         s = StringIO()
         print >> s, "%s record time: %.1f\n" % ( self.label, t )
         if self._lastIdx != -1:
            i = self._lastIdx
            while not np.isnan( self.v[0][i] ):
               print >> s, "   %.1f %.1f " % ( self.v[0][i], self.v[1][i] )
               i = self._prevIdx( i )

         self.log.debug( s.getvalue().strip() )

   #--------------------------------------------------------------------------
   def mean( self, t=None ):
      # Remove any data older than t-self._dt
      if t:
         self.updateTo( t )

      # No data in the buffer.
      if self._lastIdx == -1:
         return None
         
      # Compute the mean value and ignore any nans.
      return np.nanmean( self.v[1] )

   #--------------------------------------------------------------------------
   def sum( self, t=None ):
      # Remove any data older than t-self._dt
      if t:
         self.updateTo( t )

      # No data in the buffer.
      if self._lastIdx == -1:
         return None
         
      # Sum all the values and ignore any nans.
      return np.nansum( self.v[1] )

   #--------------------------------------------------------------------------
   def max( self, t=None ):
      # Remove any data older than t-self._dt
      if t:
         self.updateTo( t )
         
      # No data in the buffer.
      if self._lastIdx == -1:
         return None
         
      # Compute the max value and ignore any nans.
      return np.nanmax( self.v[1] )

   #--------------------------------------------------------------------------
   def min( self, t=None ):
      # Remove any data older than t-self._dt
      if t:
         self.updateTo( t )
         
      # No data in the buffer.
      if self._lastIdx == -1:
         return None
         
      # Compute the max value and ignore any nans.
      return np.nanmin( self.v[1] )

   #--------------------------------------------------------------------------
   def updateTo( self, time ):
      if self._lastIdx == -1:
         return
      
      # Delete any entries that are more than self._dt before the
      # input time.
      tBeg = time - self._dt

      # Find the indeces where the time is too old.  This returns a
      # tuple of len 1 so it can be used as an array index below.
      i = np.where( self.v[0] < tBeg )

      # Reset those values to nan
      if i:
         # Get an index of the current nan values.
         nans = np.where( np.isnan( self.v[0] ) == True )
         
         self.v[0][i] = np.nan
         self.v[1][i] = np.nan

         # If the number of existing nan values and old values is the
         # length of the array, reset lastIdx to indicate there is no
         # data.  This eliminates warnings about all-nan axis when
         # doing computations.
         if ( len( nans[0] ) + len( i[0] ) ) == self._len:
            self._lastIdx = -1
         
   #--------------------------------------------------------------------------
   def _nextIdx( self, index ):
      nextIdx = index + 1
      if nextIdx == self._len:
         nextIdx = 0

      return nextIdx
      
   #--------------------------------------------------------------------------
   def _prevIdx( self, index ):
      prevIdx = index - 1
      if prevIdx < 0:
         prevIdx = self._len - 1

      return prevIdx
      
   #--------------------------------------------------------------------------

#===========================================================================
class Reader:
   def __init__( self, config, log ):
      self.config = config
      self.log = log

      # Fields that use config.poll are used to return the average
      # value over the poll interval.  That decouples the interval we
      # get messages in and the upload reporting interval.  Some
      # fields have fixed intervals that weather underground requires
      # (like rain).
      self.temps = []
      self.tempKeys = []
      for i in range( len( config.mqttTemp ) ):
         self.temps.append( CircularTimeBuf( config.poll, config.maxRate,
                                             "Temp %d" % i, self.log ) )
         if i == 0:
            self.tempKeys.append( 'tempf' )
         else:
            self.tempKeys.append( 'temp%df' % i )
      
      self.humidity = CircularTimeBuf( config.poll, config.maxRate,
                                       "Humidity", self.log )
      self.barometer = CircularTimeBuf( config.poll, config.maxRate,
                                        "Barometer", self.log )

      # Uploaded wind speed/dir are the average over the poll interval
      # Gust values will be the maximum value over the poll interval.
      self.windSpeed = CircularTimeBuf( config.poll, config.maxRate,
                                        "Wind Speed", self.log )

      # Average direction has to be computed by averaging the vector
      # directions and then turning that back to an angle.  See:
      # http://www.webmet.com/met_monitoring/622.html
      # A weighted version is shown here - but I'm not doing that
      # because the speed and direction messages are separate - so
      # this is just the averaged direction.
      # east = speed * sin( dir )
      # north = speed * cos( dir )
      # ve = -1/n sum( east )
      # vn = -1/n sum( north )
      # Average dir = arctan( ve/vn ) +/- 180
      self.windEast = CircularTimeBuf( config.poll, config.maxRate,
                                       "Wind Dir East", self.log )
      self.windNorth = CircularTimeBuf( config.poll, config.maxRate,
                                       "Wind Dir North", self.log )

      # Accumulate rain for the day.  Store the current date when the
      # first reading shows up.  If the date changes, then we reset
      # the accumulation.
      self.rainDate = None
      self.rainDayTotal = 0.0

      # Accumulate rain for the last hour and allow at least 15
      # seconds between messages (acurite publishes every 36 seconds
      # so this is fine).
      self.rainHour = CircularTimeBuf( 3600.0, 15, "Rain Hour", self.log )

      # MQTT will be pushing data to use and we'll be publishing it
      # out so we need to lock when accessing the numpy matrix.
      self.lock = threading.Lock()

   #--------------------------------------------------------------------------
   def readMsg( self, client, userData, msg ):
      with self.lock:
         topic = msg.topic
         data = util.json.loads( msg.payload )
         self.log.info( "Read %s: %s" % ( topic, data ) )

         time = data['time']

         for i in range( len( self.config.mqttTemp ) ):
            if topic == self.config.mqttTemp[i]:
               self.temps[i].append( time, data['temperature' ] )
               break

         else:
            if topic == self.config.mqttHumidity:
               self.humidity.append( time, data['humidity' ] )

            elif topic == self.config.mqttBarometer:
               self.barometer.append( time, data['pressure' ] )

            elif topic == self.config.mqttRain:
               today = datetime.date.today()
               
               # Reset the rain if the local day changes.
               if self.rainDate != today:
                  self.rainDayTotal = 0.0
                  self.rainDate = today
                  self.log.info( "Update rain date to %s" % today )

               self.rainDayTotal += data['rain']
               self.rainHour.append( time, data['rain'] )

            elif topic == self.config.mqttWindSpeed:
               self.windSpeed.append( time, data['speed'] )

            elif topic == self.config.mqttWindDir:
               # Note: if we multiple the trig terms by the speed, it
               # would give us a weighted direction.  But that
               # requires matching the direction msg time with the
               # speed msg time and requires they both exist.  So it's
               # easier to just average the directions.
               angle = np.deg2rad( data['direction'] )
               self.windEast.append( time, np.sin( angle ) )
               self.windNorth.append( time, np.cos( angle ) )

   #--------------------------------------------------------------------------
   def updatePayload( self, payload ):
      with self.lock:
         t = time.time()
         dt = datetime.datetime.utcnow()
         payload['dateutc'] = dt.strftime( '%Y-%m-%d %H:%M:%S' )

         # Only update the payload dictionary if the value from the
         # circular buffer isn't None.  That can happen if we don't
         # have any data for the requested interval.  Round the result
         # to a few digits to keep the upload message smaller.
         def updateDict( key, value, digits=self.config.digits ):
            if value is not None:
               payload[key] = round( value, digits )

         haveData = False

         if self.windSpeed:
            haveData = True
            updateDict( 'windspeedmph', self.windSpeed.mean( t ) )
            updateDict( 'windgustmph', self.windSpeed.max( t ) )

         if self.windEast:
            # Average the wind direction using vector math.
            # See: http://www.webmet.com/met_monitoring/622.html
            avgEast = - self.windEast.mean( t )
            avgNorth = - self.windNorth.mean( t )
            windDir = np.rad2deg( np.arctan2( avgEast, avgNorth ) )
            # Shift to the correct quadrant
            if windDir < 180:
               windDir += 180
            else:
               windDir -= 180
            
            updateDict( 'winddir', windDir )

         if self.humidity:
            haveData = True
            updateDict( 'humidity', self.humidity.mean( t ) )

         if self.barometer:
            haveData = True
            updateDict( 'baromin', self.barometer.mean( t ) )

         if self.rainDate is not None:
            haveData = True
            updateDict( 'dailyrainin', self.rainDayTotal, 3 )
            updateDict( 'rainin', self.rainHour.sum( t ), 3 )

         for i in range( len( self.temps ) ):
            if self.temps[i]:
               haveData = True
               updateDict( self.tempKeys[i], self.temps[i].mean( t ) )

         return haveData
      
   #--------------------------------------------------------------------------

#===========================================================================
def start( config, client, debug=False ):
   fromts = datetime.datetime.fromtimestamp

   log = util.log.get( "weatherUnderground" )

   # URL arguments to send.
   payloadBase = {
      'action' : 'updateraw',
      'ID' : config.id,
      'PASSWORD' : config.password,
      'dateutc' : None,  # 'YYYY-MM-DD HH:MM:SS'
      # 'winddir' : 0-360
      # 'windspeedmph' : speed in mph
      # 'windgustmph' : gust in mph
      # 'humidity' : 0-100%
      # 'tempf' : temperature F
      # 'temp2f' : temperature F
      # 'rainin' :  inches of rain over the last hour
      # 'dailyrainin' : inches of rain over the local day
      # 'baromin' : barometric pressure in inches
      }
   payload = payloadBase.copy()

   # Create a reader to process weather mes sages.
   reader = Reader( config, log )
   client.on_message = reader.readMsg

   # Subscribe to all the weather topics we need to upload.
   for topic in config.mqttTemp:
      client.subscribe( topic )

   client.subscribe( config.mqttHumidity )
   client.subscribe( config.mqttBarometer )
   client.subscribe( config.mqttRain )
   client.subscribe( config.mqttWindSpeed )
   client.subscribe( config.mqttWindDir )

   # Start the MQTT as a background thread. This way we can run our
   # upload process in the rest of the code.
   client.loop_start()

   while True:
      # Fill in the current values into the payload dict.
      haveData = reader.updatePayload( payload )
      if haveData:
         try:
            log.info( "Uploading: %s" % payload )

            # Send the HTTP request.
            r = requests.get( config.uploadUrl, params=payload )
            log.debug( "URL: %s" % r.url )
            
            if r.text.strip() != "success":
               log.error( "WUG response: '%s'" % r.text )
            
         except:
            log.exception( "Upload failed to run" )

         # Clear the payload back to the minimum set of fields.
         payload = payloadBase.copy()
         
      else:
         log.info( "Ignoring send opportunity - no data" )

      # Sleep until the next time we should upload.
      time.sleep( config.poll )

#===========================================================================
