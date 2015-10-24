#===========================================================================
#
# InstantaneousDemand Message
#
#===========================================================================
from .Base import Base
from . import convert

#==========================================================================
class InstantaneousDemand ( Base ):
   """Instantaneous demand message

   After construction, will have the following attributes:
   
      DeviceMacId           int
      MeterMacId            int
      TimeStamp             float (UTC sec past 1-JAN-2000 00:00)
      Demand                float in Watt (may be negative)
      Multiplier            float
      Divisor               float
      DigitsRight           int
      DigitsLeft            int
      SuppressLeadingZero   str

      Power                 float in kWatt (may be negative)
      Time                  datetime UTC time stamp
      TimeUnix              float (UTC sec past 1-JAN-1970 00:00)

   Sample:

   <InstantaneousDemand>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <TimeStamp>0x1c531d48</TimeStamp>
     <Demand>0x00032d</Demand>
     <Multiplier>0x00000001</Multiplier>
     <Divisor>0x000003e8</Divisor>
     <DigitsRight>0x03</DigitsRight>
     <DigitsLeft>0x06</DigitsLeft>
     <SuppressLeadingZero>Y</SuppressLeadingZero>
   </InstantaneousDemand>

   plus:
      Time : datetime object
      Power : intantaneous power reading
   """
   
   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _intHexKeys = [ "DeviceMacId", "MeterMacId", "DigitsRight", "DigitsLeft" ]
   _numHexKeys = [ "Demand", "Multiplier", "Divisor", "TimeStamp" ]

   _jsonKeys = [ "DeviceMacid", "MeterMacId", "Power" ]
   
   #------------------------------------------------------------------------
   def __init__( self, node ):
      assert( node.tag == "InstantaneousDemand" )
      Base.__init__( self, "InstantaneousDemand", node )

      # Convert a 0 value to 1 (special case).
      convert.zeroToOne( self, [ "Multiplier", "Divisor" ] )

      # Handle the signed demand field.
      self.Demand = convert.toSigned4( self.Demand ) 

      self.Power = convert.toValue( self.Demand, self.Multiplier, self.Divisor )
      
      convert.time( self, "Time", "TimeUnix", self.TimeStamp )

   #------------------------------------------------------------------------

#==========================================================================
   
      
