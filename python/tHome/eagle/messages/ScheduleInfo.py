#===========================================================================
#
# ScheduleInfo Message
#
#===========================================================================
from .Base import Base

#==========================================================================
class ScheduleInfo ( Base ):
   """Schedule info message

   After construction, will have the following attributes:
   
      DeviceMacId   int
      MeterMacId    int
      Mode          str
      Event         str
      Frequency     float (sec)
      Enabled       str

   Sample:
   
   <ScheduleInfo>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <Mode>default</Mode>
     <Event>message</Event>
     <Frequency>0x00000078</Frequency>
     <Enabled>Y</Enabled>
   </ScheduleInfo>
   """

   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _numHexKeys = [ "Frequency" ]
   _intHexKeys = [ "DeviceMacId", "MeterMacId" ]

   _jsonKeys = [ "DeviceMacid", "MeterMacId", "Mode", "Event", "Frequency",
                 "Enabled" ]

   #------------------------------------------------------------------------
   def __init__( self, node ):
      """node == xml ETree node
      """
      assert( node.tag == "ScheduleInfo" )
      Base.__init__( self, "ScheduleInfo", node )

   #------------------------------------------------------------------------

#==========================================================================
   
      
