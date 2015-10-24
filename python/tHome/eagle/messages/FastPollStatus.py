#===========================================================================
#
# FastPollStatus Message
#
#===========================================================================
from .Base import Base
from . import convert

#==========================================================================
class FastPollStatus ( Base ):
   """Fast polling status message

   After construction, will have the following attributes:
   
      DeviceMacId   int
      CoordMacId    int
      Frequency     float (sec)
      EndTime       float (UTC sec past 1-JAN-2000 00:00)

      End           datetime UTC time stamp
      EndUnix       float (UTC sec past 1-JAN-1970 00:00)

   Sample:
   
   <FastPollStatus>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <Frequency>0x00</Frequency>
     <EndTime>0xFFFFFFFF</EndTime>
   </FastPollStatus>
   """

   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _numHexKeys = [ "Frequency", "EndTime" ]
   _intHexKeys = [ "DeviceMacId", "MeterMacId" ]

   _jsonKeys = [ "DeviceMacid", "Frequency" ]
   
   #------------------------------------------------------------------------
   def __init__( self, node ):
      """node == xml ETree node
      """
      assert( node.tag == "FastPollStatus" )
      Base.__init__( self, "FastPollStatus", node )

      convert.time( self, "End", "EndUnix", self.EndTime )
      
   #------------------------------------------------------------------------

#==========================================================================
   
      
