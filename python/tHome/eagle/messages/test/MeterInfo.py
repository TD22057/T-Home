#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
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

root = ET.fromstring( s )

n = E.messages.MeterInfo( root )
print n


