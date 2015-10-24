#===========================================================================
#
#  Message
#
#===========================================================================
from .Base import Base
from . import convert

#==========================================================================
class PriceCluster ( Base ):
   """Price cluster message

   After construction, will have the following attributes:
   
      DeviceMacId           int
      MeterMacId            int
      TimeStamp             float (UTC sec past 1-JAN-2000 00:00)
      Price                 float
      Currency              int
      TrailingDigits        int
      Tier                  int
      StartTime             float (UTC sec past 1-JAN-2000 00:00)
      Duration              float

      Time                  datetime UTC time stamp
      TimeUnix              float (UTC sec past 1-JAN-1970 00:00)
      Start                 datetime UTC time stamp
      StartUnix             float (UTC sec past 1-JAN-1970 00:00)
      
   Optional:
      RateLabel             str
      TierLabel             str
   
   Sample:

   <PriceCluster>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <TimeStamp>0xffffffff</TimeStamp>
     <Price>0x0000000e</Price>
     <Currency>0x0348</Currency>
     <TrailingDigits>0x02</TrailingDigits>
     <Tier>0x01</Tier>
     <StartTime>0xffffffff</StartTime>
     <Duration>0xffff</Duration>
     <RateLabel>Tier 1</RateLabel>
   </PriceCluster>
   """
   
   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _intHexKeys = [ "DeviceMacId", "MeterMacId", "Currency", "TrailingDigits",
                   "Tier" ]
   _numHexKeys = [ "TimeStamp", "StartTime", "Price", "Duration" ]
   
   _jsonKeys = [ "DeviceMacid", "MeterMacId", "Time", "Price", "Tier" ]
   
   #------------------------------------------------------------------------
   def __init__( self, node ):
      assert( node.tag == "PriceCluster" )
      Base.__init__( self, "PriceCluster", node )

      if self.Price == 0xffffffff:
         self.Price = 0.0
         
      self.Price = self.Price / 10**self.TrailingDigits
      
      convert.time( self, "Time", "TimeUnix", self.TimeStamp )
      convert.time( self, "Start", "StartUnix", self.StartTime )

   #------------------------------------------------------------------------

#==========================================================================
   
      
