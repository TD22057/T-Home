#===========================================================================
#
# Radio thermostat device configuration
#
#===========================================================================
# Time in seconds to poll the thermostat
pollTime = 60

# Thermostats to poll.  Keys are:
#    host            thermostat IP address
#    label           label to use in logs and messages.
#    mqttTempTopic   MQTT topic to publish current temp messages to.
#    mqttModeTopic   MQTT topic to publish mode changes to.
#    mqttStateTopic  MQTT topic to publish state (on/off) changes to.
#    mqttSetTopic    MQTT topic to subscribe to read requests to change
#                    the thermostat.
#
thermostats = [
   {
      'host' : '192.168.1.15',
      'label' : 'Downstairs',
      'mqttTempTopic' : 'env/temp/Living Room',
      'mqttModeTopic' : 'hvac/Living Room/mode',
      'mqttStateTopic' : 'hvac/Living Room/state',
      'mqttSetTopic' : 'hvac/Living Room/set/+',
      },
   {
      'host' : '192.168.1.16',
      'label' : 'Upstairs',
      'mqttTempTopic' : 'env/temp/Master Bedroom',
      'mqttModeTopic' : 'hvac/Master Bedroom/mode',
      'mqttStateTopic' : 'hvac/Master Bedroom/state',
      'mqttSetTopic' : 'hvac/Master Bedroom/set/+',
     },
   ]

#===========================================================================
#
# Logging configuration
#
#===========================================================================
logFile = '/var/log/tHome/thermostat.log'
logLevel = 40


