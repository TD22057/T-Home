#!/usr/bin/env python

from tHome import acurite

sensorMap = {}

for l in open( "/home/ted/weather.log", "r" ):
   p = acurite.decode( l, sensorMap )
   if p:
      print p
      
