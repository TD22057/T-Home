#!/usr/bin/env python

import xml.etree.ElementTree as ET
import tHome.eagle as E

s="""
   <BlockPriceDetail>
     <DeviceMacId>0xd8d5b9000000103f</DeviceMacId>
     <MeterMacId>0x000781000086d0fe</MeterMacId>
     <TimeStamp>0x1c531d6b</TimeStamp>
     <CurrentStart>0x00000000</CurrentStart>
     <CurrentDuration>0x0000</CurrentDuration>
     <BlockPeriodConsumption>0x0000000000231c38</BlockPeriodConsumption>
     <BlockPeriodConsumptionMultiplier>0x00000001</BlockPeriodConsumptionMultiplier>
     <BlockPeriodConsumptionDivisor>0x000003e8</BlockPeriodConsumptionDivisor>
     <NumberOfBlocks>0x00</NumberOfBlocks>
     <Multiplier>0x00000001</Multiplier>
     <Divisor>0x00000001</Divisor>
     <Currency>0x0348</Currency>
     <TrailingDigits>0x00</TrailingDigits>
   </BlockPriceDetail>
"""

root = ET.fromstring( s )

n = E.messages.BlockPriceDetail( root )
print n


