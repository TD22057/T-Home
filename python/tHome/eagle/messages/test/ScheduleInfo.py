#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
   <ScheduleInfo>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <Mode>default</Mode>
     <Event>message</Event>
     <Frequency>0x00000078</Frequency>
     <Enabled>Y</Enabled>
   </ScheduleInfo>
"""

root = ET.fromstring( s )

n = E.messages.ScheduleInfo( root )
print n


