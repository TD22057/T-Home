import os
#===========================================================================
#
# Weather underground configuration
#
#===========================================================================

# PWD upload URL and log in information.  See this url for details:
#   http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
uploadUrl = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"

id = os.environ[ "THOME_WUG_STATION" ]
password = os.environ[ "THOME_WUG_PASSWORD" ]

# Upload interval in seconds.  WUG doesn't really support high rate
# data so 1-2 minutes is fine.
poll = 180

# Maximum expected sensor input rate.  System will store poll/maxRate
# values in a circular buffer and average the last set of values to up
# load.  So if poll is 120 and maxRate is 10, a buffer with 12 values
# will be created.  As data is received, it will be inserted into the
# buffer and the last n values (up to 12) since the last upload will
# be averaged to get the value to upload.  Some values like wind gust
# will use the maximum value in the interval instead of the average.
# Rain values are accumulated, not averaged.
maxRate = 10

# Number of floating point digits to the right of the decimal to round
# values to before uploading them.
digits = 2

#===========================================================================
#
# MQTT topic names.  These are the sensors to upload.
#
#===========================================================================
# List of temperature topics to report as outdoor temperatures.
mqttTemp = [
   "env/temp/Backyard",
   "env/temp/Courtyard",
   ]

mqttHumidity = 'env/humidity/Backyard'
mqttBarometer = 'env/barometer/Bridge'
mqttRain = 'env/rain/Backyard'
mqttWindSpeed = 'env/wind/speed/Backyard'
mqttWindDir = 'env/wind/direction/Backyard'

#===========================================================================
#
# Logging configuration
#
#===========================================================================
logFile = '/var/log/tHome/weatherUnderground.log'
logLevel = 20

