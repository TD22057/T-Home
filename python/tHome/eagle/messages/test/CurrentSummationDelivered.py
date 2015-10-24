#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
   <CurrentSummationDelivered>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <TimeStamp>0x1c531e54</TimeStamp>
     <SummationDelivered>0x0000000001321a5f</SummationDelivered>
     <SummationReceived>0x00000000003f8240</SummationReceived>
     <Multiplier>0x00000001</Multiplier>
     <Divisor>0x000003e8</Divisor>
     <DigitsRight>0x01</DigitsRight>
     <DigitsLeft>0x06</DigitsLeft>
     <SuppressLeadingZero>Y</SuppressLeadingZero>
   </CurrentSummationDelivered>
"""

root = ET.fromstring( s )

n = E.messages.CurrentSummation( root )
print n


