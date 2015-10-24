#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
   <Reading>
     <Value>-123.345</Value>
     <TimeStamp>0x1c531d48</TimeStamp>
     <Type>Summation</Type>
   </Reading>
"""

root = ET.fromstring( s )

n = E.messages.Reading( root )
print n


