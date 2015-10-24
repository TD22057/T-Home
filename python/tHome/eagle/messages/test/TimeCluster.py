#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
   <TimeCluster>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <UTCTime>0x1c531da7</UTCTime>
     <LocalTime>0x1c52ad27</LocalTime>
   </TimeCluster>
"""

root = ET.fromstring( s )

n = E.messages.TimeCluster( root )
print n


