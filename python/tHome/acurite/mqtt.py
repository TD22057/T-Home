#===========================================================================
#
# Convert decoded data to MQTT messages.
#
#===========================================================================

#===========================================================================
def convert( config, data ):
   # List of tuples of ( topic, payload ) where payload is a dictionary.
   msgs = []

   if hasattr( data, "battery" ):
      topic = config.mqttBattery % data.location
      payload = {
         "time" : data.time,
         "battery" : data.battery,
         }
      msgs.append( ( topic, payload ) )

   if hasattr( data, "signal" ):
      topic = config.mqttRssi % data.location
      payload = {
         "time" : data.time,
         # Input is 0->1, convert to 0->100
         "rssi" : data.signal * 100,
         }
      msgs.append( ( topic, payload ) )

   if hasattr( data, "humidity" ):
      topic = config.mqttHumidity % data.location
      payload = {
         "time" : data.time,
         "humidity" : data.humidity,
         }
      msgs.append( ( topic, payload ) )
   
   if hasattr( data, "temperature" ):
      topic = config.mqttTemp % data.location
      payload = {
         "time" : data.time,
         "temperature" : data.temperature,
         }
      msgs.append( ( topic, payload ) )

   if hasattr( data, "windSpeed" ):
      topic = config.mqttWindSpeed % data.location
      payload = {
         "time" : data.time,
         "speed" : data.windSpeed,
         }
      msgs.append( ( topic, payload ) )

   if hasattr( data, "windDir" ):
      topic = config.mqttWindDir % data.location
      payload = {
         "time" : data.time,
         "direction" : data.windDir,
         }
      msgs.append( ( topic, payload ) )

   if hasattr( data, "pressure" ):
      topic = config.mqttBarometer % data.location
      payload = {
         "time" : data.time,
         "pressure" : data.pressure,
         }
      msgs.append( ( topic, payload ) )

   if hasattr( data, "rainfall" ):
      topic = config.mqttRain % data.location
      payload = {
         "time" : data.time,
         "rain" : data.rainfall,
         }
      msgs.append( ( topic, payload ) )

   return msgs

#===========================================================================
