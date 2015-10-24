#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
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

root = ET.fromstring( s )

n = E.messages.DeviceInfo( root )
print n


