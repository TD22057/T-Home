#===========================================================================
#
# BlockPriceDetail Message
#
#===========================================================================
from .Base import Base
from . import convert

#==========================================================================
class BlockPriceDetail ( Base ):
   """Block price detail message

   After construction, will have the following attributes:
   
      DeviceMacId           int
      MeterMacId            int
      TimeStamp             float (UTC sec past 1-JAN-2000 00:00)
      CurrentStart
      CurrentDuration
      BlockPeriodConsumption
      BlockPeriodConsumptionMultiplier
      BlockPeriodConsumptionDivisor
      NumberOfBlocks
      Multiplier
      Divisor
      Currency
      TrailingDigits

      Time                  datetime UTC time stamp
      TimeUnix              float (UTC sec past 1-JAN-1970 00:00)
      Consumption
   
   Sample:
   <BlockPriceDetail>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <TimeStamp>0x1c531d6b</TimeStamp>
     <CurrentStart>0x00000000</CurrentStart>
     <CurrentDuration>0x0000</CurrentDuration>
     <BlockPeriodConsumption>0x0000000000231c38</BlockPeriodConsumption>
     <BlockPeriodConsumptionMultiplier>0x00000001</BlockPeriodConsumptionMultiplier>
     <BlockPeriodConsumptionDivisor>0x000003e8</BlockPeriodConsumptionDivisor>
     <NumberOfBlocks>0x00</NumberOfBlocks>
     <Multiplier>0x00000001</Multiplier>
     <Divisor>0x00000001</Divisor>
     <Currency>0x0348</Currency>
     <TrailingDigits>0x00</TrailingDigits>
   </BlockPriceDetail>
   """
   
   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _intHexKeys = [ "DeviceMacId", "MeterMacId", "NumberOfBlocks", "Currency",
                   "TrailingDigits", ]
   _numHexKeys = [ "TimeStamp", "CurrentStart", "CurrentDuration",
                   "BlockPeriodConsumption", "BlockPeriodConsumptionMultiplier",
                   "BlockPeriodConsumptionDivisor", "Multiplier", "Divisor" ]
   
   _jsonKeys = [ "DeviceMacid", "MeterMacId", "Consumption" ]
   
   #------------------------------------------------------------------------
   def __init__( self, node ):
      assert( node.tag == "BlockPriceDetail" )
      Base.__init__( self, "BlockPriceDetail", node )

      # Convert a 0 value to 1 (special case).
      convert.zeroToOne( self, [ "Multiplier", "Divisor" ] )
      convert.zeroToOne( self, [ "BlockPeriodConsumptionMultiplier",
                                 "BlockPeriodConsumptionDivisor" ] )
      
      self.Consumption = convert.toValue( self.BlockPeriodConsumption,
                                          self.BlockPeriodConsumptionMultiplier,
                                          self.BlockPeriodConsumptionDivisor )
      
      convert.time( self, "Time", "TimeUnix", self.TimeStamp )

   #------------------------------------------------------------------------
   def jsonMsg( self ):
      return {
         "MacId" : self.DeviceMacId,
         "Time" : self.TimeUnix,
         "Consumption" : self.Consumption,
         }
         
#==========================================================================
   
      
