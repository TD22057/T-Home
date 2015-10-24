#===========================================================================
#
# Field conversion utilities.
#
#===========================================================================
import datetime

#==========================================================================

# Eagle reference date as a datetime object.
eagleT0 = datetime.datetime( 2000, 1, 1 )

# Delta in seconds between Eagle ref and UNIX ref time.
eagleT0_unixT0 = ( eagleT0 - datetime.datetime( 1970, 1, 1 ) ).total_seconds()

#==========================================================================
def hexKeys( obj, keyList, cvtFunc ):
   for key in keyList:
      strVal = getattr( obj, key, None )
      if strVal is None:
         continue
      
      intVal = int( strVal, 16 )
      setattr( obj, key, cvtFunc( intVal ) )

#==========================================================================
def time( obj, timeKey, unixKey, eagleSec ):
   timeValue = None
   unixValue = None
   if eagleSec:
      timeValue = toDateTime( eagleSec )
      unixValue = toUnixTime( eagleSec )

   setattr( obj, timeKey, timeValue )
   setattr( obj, unixKey, unixValue )
      
   
#==========================================================================
def zeroToOne( obj, keyList ):
   for key in keyList:
      val = getattr( obj, key )
      if not val:
         setattr( obj, key, 1.0 )

#==========================================================================
def toValue( value, multiplier, divisor ):
   return float( value ) * multiplier / divisor

#==========================================================================
def toSigned4( value ):
   if value > 0x7FFFFFFF:
      return value - 0xFFFFFFFF
   return value


#==========================================================================
def toUnixTime( eagleSec ):
   """Input is EAGLE UTC seconds past 00:00:00 1-jan-2000

   Returns a float of UTC seconds past UTC 1-jan-1970.
   """
   return eagleSec + eagleT0_unixT0

#==========================================================================
def toDateTime( eagleSec ):
   """Input is EAGLE UTC seconds past 00:00:00 1-jan-2000

   Returns a datetime object
   """
   return eagleT0 + datetime.timedelta( 0, float( eagleSec ) )

#==========================================================================
def fromTime( dateTime ):
   "datetime object MUST be utc"
   dt = dateTime - eagleT0
   isec = int(  dt.total_seconds() )
   return hex( isec )
   
#==========================================================================

