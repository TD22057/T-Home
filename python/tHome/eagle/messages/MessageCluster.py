#===========================================================================
#
# MessageCluster Message
#
#===========================================================================
from .Base import Base
from . import convert

#==========================================================================
class MessageCluster ( Base ):
   """Message cluster message

   After construction, will have the following attributes:
   
      DeviceMacId           int
      MeterMacId            int
      TimeStamp             float (UTC sec past 1-JAN-2000 00:00)
      Id                    int
      Text                  str
      Priority              str
      StartTime             float (UTC sec past 1-JAN-2000 00:00)
      Duration              float
      ConfirmationRequired  str
      Confirmed             str
      Queue                 str

      Time                  datetime UTC time stamp
      TimeUnix              float (UTC sec past 1-JAN-1970 00:00)
      Start                 datetime UTC time stamp
      StartUnix             float (UTC sec past 1-JAN-1970 00:00)
      
   Sample:

   <MessageCluster>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <TimeStamp></TimeStamp>
     <Id></Id>
     <Text></Text>
     <Priority></Priority>
     <StartTime></StartTime>
     <Duration></Duration>
     <ConfirmationRequired>N</ConfirmationRequired>
     <Confirmed>N</Confirmed>
     <Queue>Active</Queue>
   </MessageCluster>
   """
   
   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _intHexKeys = [ "DeviceMacId", "MeterMacId", "Id" ]
   _numHexKeys = [ "TimeStamp", "StartTime", "Duration" ]
   
   _jsonKeys = [ "DeviceMacid", "MeterMacId", "Id", "Text", "Priority",
                 "Duration", "StartTime", "Queue" ]
   
   #------------------------------------------------------------------------
   def __init__( self, node ):
      assert( node.tag == "MessageCluster" )
      Base.__init__( self, "MessageCluster", node )

      convert.time( self, "Time", "TimeUnix", self.TimeStamp )
      convert.time( self, "Start", "StartUnix", self.StartTime )
      
   #------------------------------------------------------------------------

#==========================================================================
   
      
