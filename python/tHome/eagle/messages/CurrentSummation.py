#===========================================================================
#
# CurrentSummation Message
#
#===========================================================================
from .Base import Base
from . import convert

#==========================================================================
class CurrentSummation ( Base ):
   """Current summation message

   After construction, will have the following attributes:
   
      DeviceMacId           int
      MeterMacId            int
      TimeStamp             float (UTC sec past 1-JAN-2000 00:00)
      SummationDelivered    float (utility->user)
      SummationReceived     float (user->utility)
      Multiplier            float
      Divisor               float
      DigitsRight           int
      DigitsLeft            int
      SuppressLeadingZero   str

      Consumed              float in kWh (utility->user)
      Produced              float in kWh (user->utility)
      Time                  datetime UTC time stamp
      TimeUnix              float (UTC sec past 1-JAN-1970 00:00)
   
   Sample:

   NOTE: Socket API uses CurrentSummation, uploader (cloud) API uses
   CurrentSummationDelivered.  Both are fine.
   
   <CurrentSummationDelivered>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <TimeStamp>0x1c531e54</TimeStamp>
     <SummationDelivered>0x0000000001321a5f</SummationDelivered>
     <SummationReceived>0x00000000003f8240</SummationReceived>
     <Multiplier>0x00000001</Multiplier>
     <Divisor>0x000003e8</Divisor>
     <DigitsRight>0x01</DigitsRight>
     <DigitsLeft>0x06</DigitsLeft>
     <SuppressLeadingZero>Y</SuppressLeadingZero>
   </CurrentSummationDelivered>
   """
   
   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _intHexKeys = [ "DeviceMacId", "MeterMacId", "DigitsRight", "DigitsLeft" ]
   _numHexKeys = [ "TimeStamp", "SummationDelivered", "SummationReceived",
                   "Multiplier", "Divisor" ]

   _jsonKeys = [ "DeviceMacid", "MeterMacId", "Consumed", "Produced" ]
   
   #------------------------------------------------------------------------
   def __init__( self, node ):
      assert( node.tag == "CurrentSummation" or
              node.tag == "CurrentSummationDelivered" )
      Base.__init__( self, "CurrentSummation", node )

      # Convert a 0 value to 1 (special case).
      convert.zeroToOne( self, [ "Multiplier", "Divisor" ] )

      self.Consumed = convert.toValue( self.SummationDelivered,
                                       self.Multiplier, self.Divisor )
      self.Produced = convert.toValue( self.SummationReceived,
                                       self.Multiplier, self.Divisor )
      
      convert.time( self, "Time", "TimeUnix", self.TimeStamp )

   #------------------------------------------------------------------------

#==========================================================================
   
      
