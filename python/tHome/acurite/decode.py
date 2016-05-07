#===========================================================================
#
# Acurite sensor data class
#
#===========================================================================
import StringIO
import time
from ..util import Data

#------------------------------------------------------------------------
windMap = {
   '5' : 0,
   '7' : 22.5,
   '3' : 45,
   '1' : 67.5,
   '9' : 90,
   'B' : 112.5,
   'F' : 135,
   'D' : 157.5,
   'C' : 180,
   'E' : 202.5,
   'A' : 225,
   '8' : 247.5,
   '0' : 270,
   '2' : 292.5,
   '6' : 315,
   '4' : 337.5,
   }

#------------------------------------------------------------------------
batteryMap = {
   "normal" : 1.0,
   "low" : 0.1,
   }

#===========================================================================
def decode( text, sensorMap ):
   """Decode a sensor post from the Acurite bridge.

   Input is a line of text sent by the bridge to the Acurite server.
   Return valeue is a tHome.util.Data object (dict) with the parsed
   values.
   """
   # Skip lines that aren't the sensor information.
   idx = text.find( "id=" )
   if idx == -1:
      return

   text = text[idx:]

   # Split the input into fields.
   elems = text.split( "&" )

   # Get the key/value pairs for each element.
   items = {}
   for e in elems:
      k, v = e.split( "=" )
      items[k] = v

   # Create an empty data object (dict) to store the results.
   data = Data()

   # No time field in the data - record the current time as the time
   # stamp.
   data.time = time.time()

   # Call the handler function for each element.
   for k, v in items.iteritems():
      func = handlers.get( k, None )
      if func:
         func( data, items, k, v )

   # Use the sensor map to process the data.  This primarily sets a
   # location label given the sensor ID field.
   s = sensorMap.get( data.id, None )
   if s:
      s.process( data )
   else:
      data.location = "Unknown"

   return data

#===========================================================================
def _readSensor( data, items, key, value ):
   data.id = value
      
#===========================================================================
def _readPressure( data, items, key, value ):
   if value != "pressure":
      return

   # Convert hex strings to integer values
   c1 = int( items["C1"], 16 )
   c2 = int( items["C2"], 16 )
   c3 = int( items["C3"], 16 )
   c4 = int( items["C4"], 16 )
   c5 = int( items["C5"], 16 )
   c6 = int( items["C6"], 16 )
   c7 = int( items["C7"], 16 )
   a = int( items["A"], 16 )
   b = int( items["B"], 16 )
   c = int( items["C"], 16 )
   d = int( items["D"], 16 )
   pr = int( items["PR"], 16 )
   tr = int( items["TR"], 16 )

   if tr >= c5:
      dut = tr - c5 - (tr-c5)/128.0 * (tr-c5)/128.0 * a/2**c
   else:
      dut = tr - c5 - (tr-c5)/128.0 * (tr-c5)/128.0 * b/2**c

   off = (c2 + (c4 - 1024) * dut / 16384.0) * 4
   sens = c1 + c3 * dut / 1024.0
   x = sens * (pr - 7168) / 16384.0 - off
   p = x * 10 / 32 + c7 + 760.0

   data.id = items.get( "id", "Unknown" )
   data.pressure = round( p / 338.637526, 2 )  # Convert to HgIn      
   
#===========================================================================
def _readSignal( data, items, key, value ):
   data.signal = float( value ) / 4.0
   
#===========================================================================
def _readBattery( data, items, key, value ):
   data.battery = batteryMap.get( value, 0 )

#===========================================================================
def _readWindDir( data, items, key, value ):
   data.windDir = windMap.get( value, None )

#===========================================================================
def _readWindSpeed( data, items, key, value ):
   """ A0aaaabbbbb == aaaa.bbbbb cm/sec
   """
   cmPerSec = float( value[2:6] ) + float( value[6:10] ) / 1e4
   data.windSpeed = round( cmPerSec / 44.704, 2 )

#===========================================================================
def _readTemp( data, items, key, value ):
   """ Aaaabbbbbb == aaa.bbbbbb deg C
   """
   degC = float( value[1:4] ) + float( value[4:10] ) / 1e6
   data.temperature = round( degC * 1.8 + 32, 1 )

#===========================================================================
def _readHumidity( data, items, key, value ):
   """ Aaaabbbbbb == aaa.bbbbbb percentage
   """
   data.humidity = float( value[1:4] ) + float( value[4:10] ) / 1e6

#===========================================================================
def _readRainfall( data, items, key, value ):
   """ A0aabbbb == aa.bbbb cm in the last 36 seconds
   """
   cm = float( value[2:4] ) + float( value[4:8] ) / 1e4
   data.rainfall = round( cm / 25.4, 3 )

#===========================================================================
handlers = {
   "sensor" : _readSensor,
   "mt" : _readPressure,
   "windspeed" : _readWindSpeed,
   "winddir" : _readWindDir,
   "temperature" : _readTemp,
   "humidity" : _readHumidity,
   "rainfall" : _readRainfall,
   "battery" : _readBattery,
   "rssi" : _readSignal,
   }

#===========================================================================
