#===========================================================================
#
# Sensor configuration class
#
#===========================================================================

#===========================================================================
class Sensor:
   """Sensor msg processer.

   Set humidity to False for temp only sensors to clear the humidity
   field.  The bridge reports humidity of 16% for these sensors which
   is incorrrect.
   """
   def __init__( self, id, location, humidity=True ):
      self.id = id
      self.location = location
      self.hasHumidity = humidity

   #------------------------------------------------------------------------
   def process( self, msg ):
      assert( self.id == msg.id )
      msg.location = self.location

      # Remove the humidity attribute if the sensor doesn't suppor it.
      if not self.hasHumidity and hasattr( msg, "humidity" ):
         del msg.humidity

#===========================================================================

