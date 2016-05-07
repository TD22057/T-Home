#!/usr/bin/env python

from tHome import acurite

sensors = [
   acurite.Sensor( "08260", "Garage" ),
   acurite.Sensor( "09096", "Kitchen" ),
   acurite.Sensor( "00414", "Backyard" ),
   acurite.Sensor( "24C86E0449A0", "Bridge" ),
   acurite.Sensor( "05250", "Courtyard", humidity=False ),
   acurite.Sensor( "16039", "Rec Room", humidity=False ),
   acurite.Sensor( "02717", "Front Bedroom", humidity=False ),
   acurite.Sensor( "05125", "Den", humidity=False ),
   acurite.Sensor( "08628", "Garage 2", humidity=False ),
   acurite.Sensor( "09338", "Side Bedroom", humidity=False ),
   acurite.Sensor( "01948", "Master Closet", humidity=False ),
   acurite.Sensor( "15116", "Attic", humidity=False ),
   acurite.Sensor( "05450", "Master Bath", humidity=False ),
   ]

sensorMap = {}
for s in sensors:
   sensorMap[s.id] = s

for l in open( "/home/ted/weather.log", "r" ):
   r = acurite.cmdLine.process( l, sensorMap )
   if r:
      print r
      
