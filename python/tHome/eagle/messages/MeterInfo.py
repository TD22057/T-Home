#===========================================================================
#
# MeterInfo Message
#
#===========================================================================
from .Base import Base

#==========================================================================
class MeterInfo ( Base ):
   """Network info message

   After construction, will have the following attributes:
   
      DeviceMacId   int
      CoordMacId    int
      Type          str
      Nickname      str
  Optional:
      Account       str
      Auth          str
      Host          str
      Enabled       str

   Sample:
   <MeterInfo>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <Type>0x0000</Type>
     <Nickname></Nickname>
     <Account></Account>
     <Auth></Auth>
     <Host></Host>
     <Enabled>Y</Enabled>
   </MeterInfo>
   """

   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _numHexKeys = []
   _intHexKeys = [ "DeviceMacId", "CoordMacId" ]

   _jsonKeys = [ "DeviceMacid", "Type", "Enabled" ]
   
   #------------------------------------------------------------------------
   def __init__( self, node ):
      """node == xml ETree node
      """
      assert( node.tag == "MeterInfo" )
      Base.__init__( self, "MeterInfo", node )

   #------------------------------------------------------------------------

#==========================================================================
   
      
