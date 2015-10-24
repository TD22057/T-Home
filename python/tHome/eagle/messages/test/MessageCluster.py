#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
   <MessageCluster>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <TimeStamp></TimeStamp>
     <Id></Id>
     <Text></Text>
     <Priority></Priority>
     <StartTime></StartTime>
     <Duration></Duration>
     <ConfirmationRequired>N</ConfirmationRequired>
     <Confirmed>N</Confirmed>
     <Queue>Active</Queue>
   </MessageCluster>
"""

root = ET.fromstring( s )

n = E.messages.MessageCluster( root )
print n


