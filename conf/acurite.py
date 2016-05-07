#===========================================================================
#
# Port to use for the web server.  Configure the ebtables/iptables
# rules to redirect Acurite Bridge posts to this port.
#
# NOTE: The port specified in the script tHome/bin/tHome-acurite.py
# must match this port.  If you change one, change the other.
#
#===========================================================================
httpPort = 22041

#===========================================================================
#
# Acurite sensor configuration
#
#===========================================================================
import tHome.acurite as A

# Sensors list.
#
# ID is the Acurite sensor ID (easiest to find by running the message
# debugger and watching them come through).
sensors = [
   # sensor ID, location label, optional args
   A.Sensor( "08260", "Garage" ),
   A.Sensor( "09096", "Kitchen" ),
   A.Sensor( "00414", "Backyard" ),
   A.Sensor( "24C86E0449A0", "Bridge" ),
   A.Sensor( "05250", "Courtyard", humidity=False ),
   A.Sensor( "16039", "Rec Room", humidity=False ),
   A.Sensor( "02717", "Front Bedroom", humidity=False ),
   A.Sensor( "05125", "Den", humidity=False ),
   A.Sensor( "08628", "Garage 2", humidity=False ),
   A.Sensor( "09338", "Side Bedroom", humidity=False ),
   A.Sensor( "01948", "Master Closet", humidity=False ),
   A.Sensor( "15116", "Attic", humidity=False ),
   A.Sensor( "05450", "Master Bath", humidity=False ),
   ]

#===========================================================================
#
# MQTT Topics.  Each requires one %s in the topic which will be
# replaced by the location string from the sensor list above.
#
#===========================================================================
mqttBattery = "power/battery/%s"
mqttRssi = "radio/%s"
mqttHumidity = "env/humidity/%s"
mqttTemp = "env/temp/%s"
mqttWindSpeed = "env/wind/speed/%s"
mqttWindDir = "env/wind/direction/%s"
mqttBarometer = "env/barometer/%s"
mqttRain = "env/rain/%s"

#===========================================================================
#
# Logging configuration
#
#===========================================================================
logFile = '/var/log/tHome/acurite.log'
logLevel = 40


