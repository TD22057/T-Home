#===========================================================================
#
# TimeCluster Message
#
#===========================================================================
from .Base import Base
from . import convert

#==========================================================================
class TimeCluster ( Base ):
   """Time cluster message

   After construction, will have the following attributes:
   
      DeviceMacId           int
      MeterMacId            int
      UTCTime               float (UTC sec past 1-JAN-2000 00:00)
      LocalTime             float (Local sec past 1-JAN-2000 00:00)

      Time                  datetime UTC time stamp
      TimeUnix              float (UTC sec past 1-JAN-1970 00:00)
      Local                 datetime local time stamp
      LocalUnix             float (local sec past 1-JAN-1970 00:00)
      
   Sample:
   
   <TimeCluster>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <UTCTime>0x1c531da7</UTCTime>
     <LocalTime>0x1c52ad27</LocalTime>
   </TimeCluster>
   """
   
   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _intHexKeys = [ "DeviceMacId", "MeterMacId" ]
   _numHexKeys = [ "UTCTime", "LocalTime" ]

   _jsonKeys = [ "DeviceMacid", "MeterMacId", "LocalUnix" ]
   
   #------------------------------------------------------------------------
   def __init__( self, node ):
      assert( node.tag == "TimeCluster" )
      Base.__init__( self, "TimeCluster", node )

      convert.time( self, "Time", "TimeUnix", self.UTCTime )
      convert.time( self, "Local", "LocalUnix", self.LocalTime )
      
   #------------------------------------------------------------------------

#==========================================================================
   
      
