#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
   <FastPollStatus>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <Frequency>0x00</Frequency>
     <EndTime>0xFFFFFFFF</EndTime>
   </FastPollStatus>
"""

root = ET.fromstring( s )

n = E.messages.FastPollStatus( root )
print n


