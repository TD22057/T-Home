#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
   <InstantaneousDemand>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <TimeStamp>0x1c531d48</TimeStamp>
     <Demand>0x00032d</Demand>
     <Multiplier>0x00000001</Multiplier>
     <Divisor>0x000003e8</Divisor>
     <DigitsRight>0x03</DigitsRight>
     <DigitsLeft>0x06</DigitsLeft>
     <SuppressLeadingZero>Y</SuppressLeadingZero>
   </InstantaneousDemand>
"""

root = ET.fromstring( s )

n = E.messages.InstantaneousDemand( root )
print n


