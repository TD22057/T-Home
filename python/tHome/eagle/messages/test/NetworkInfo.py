#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
   <NetworkInfo>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <CoordMacId>0x000781000086d0fe</CoordMacId>
     <Status>Connected</Status>
     <Description>Successfully Joined</Description>
     <ExtPanId>0x000781000086d0fe</ExtPanId>
     <Channel>20</Channel>
     <ShortAddr>0xe1aa</ShortAddr>
     <LinkStrength>0x64</LinkStrength>
   </NetworkInfo>
"""

root = ET.fromstring( s )

n = E.messages.NetworkInfo( root )
print n


