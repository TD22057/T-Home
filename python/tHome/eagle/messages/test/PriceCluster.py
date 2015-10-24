#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
   <PriceCluster>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <TimeStamp>0xffffffff</TimeStamp>
     <Price>0x0000000e</Price>
     <Currency>0x0348</Currency>
     <TrailingDigits>0x02</TrailingDigits>
     <Tier>0x01</Tier>
     <StartTime>0xffffffff</StartTime>
     <Duration>0xffff</Duration>
     <RateLabel>Tier 1</RateLabel>
   </PriceCluster>
"""

root = ET.fromstring( s )

n = E.messages.PriceCluster( root )
print n


