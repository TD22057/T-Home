#===========================================================================
#
# NetworkInfo Message
#
#===========================================================================
from .Base import Base

#==========================================================================
class NetworkInfo ( Base ):
   """Network info message

   After construction, will have the following attributes:
   
      DeviceMacId   int
      CoordMacId    int
      Status        str
      LinkStrength  int
  Optional:
      Description   str
      ExtPanId      int
      Channel       int
      ShortAddr     int

   Sample:
   
   <NetworkInfo>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <CoordMacId>0x000781000086d0fe</CoordMacId>
     <Status>Connected</Status>
     <Description>Successfully Joined</Description>
     <ExtPanId>0x000781000086d0fe</ExtPanId>
     <Channel>20</Channel>
     <ShortAddr>0xe1aa</ShortAddr>
     <LinkStrength>0x64</LinkStrength>
   </NetworkInfo>
   """

   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _numHexKeys = []
   _intHexKeys = [ "DeviceMacId", "CoordMacId", "ExtPanId", "ShortAddr",
                   "StatusCode", "LinkStrength" ]

   _jsonKeys = [ "DeviceMacid", "Status", "LinkStrength", "Description",
                 "Channel" ]
   
   #------------------------------------------------------------------------
   def __init__( self, node ):
      """node == xml ETree node
      """
      assert( node.tag == "NetworkInfo" )
      Base.__init__( self, "NetworkInfo", node )

      # Convert channel string to integer.
      if hasattr( self, "Channel" ):
         self.Channel = int( self.Channel )


   #------------------------------------------------------------------------

#==========================================================================
   
      
