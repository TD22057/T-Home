#===========================================================================
#
# DeviceInfo Message
#
#===========================================================================
from .Base import Base

#==========================================================================
class DeviceInfo ( Base ):
   """Network info message

   After construction, will have the following attributes:
   
      DeviceMacId       int
      InstallCode       int
      LinkKey           int
      FWVersion         str
      HWVersion         str
      ImageType         int 
      Manufacturer      str
      ModelId           str
      DateCode          str
      Port              str

   Sample:
   
   <DeviceInfo>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <InstallCode>0x8ba7f1dee6c4f5cc</InstallCode>
     <LinkKey>0x2b26f9124113b1e2b317d402ed789a47</LinkKey>
     <FWVersion>1.4.47 (6798)</FWVersion>
     <HWVersion>1.2.3</HWVersion>
     <ImageType>0x1301</ImageType>
     <Manufacturer>Rainforest Automation, Inc.</Manufacturer>
     <ModelId>Z109-EAGLE</ModelId>
     <DateCode>2013103023220630</DateCode>
     <Port>/dev/ttySP0</Port>
   </DeviceInfo>
   """
   
   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _numHexKeys = []
   _intHexKeys = [ "DeviceMacId", "InstallCode", "LinkKey", "ImageType" ]
   
   _jsonKeys = [ "DeviceMacid", "InstallCode", "LinkKey", "FWVersion",
                 "HWVersion", "ImageType", "Manufacturer", "ModelId",
                 "DateCode", "Port" ]
   
   #------------------------------------------------------------------------
   def __init__( self, node ):
      assert( node.tag == "DeviceInfo" )
      Base.__init__( self, "DeviceInfo", node )

   #------------------------------------------------------------------------

#==========================================================================
   
      
