#===========================================================================
#
# Config file
#
#===========================================================================

__doc__ = """Config file parsing.
"""

from .. import util
from ..util import config as C

#===========================================================================

# Config file section name and defaults.
configEntries = [
   # ( name, converter function, default value )
   C.Entry( "logFile", util.path.expand ),
   C.Entry( "logLevel", int, 20 ), # INFO
   C.Entry( "sensors", list ),
   C.Entry( "mqttBattery", str ),
   C.Entry( "mqttRssi", str ),
   C.Entry( "mqttHumidity", str ),
   C.Entry( "mqttTemp", str ),
   C.Entry( "mqttWindSpeed", str ),
   C.Entry( "mqttWindDir", str ),
   C.Entry( "mqttBarometer", str ),
   C.Entry( "mqttRain", str ),
   ]

#===========================================================================
def parse( configDir, configFile='acurite.py' ):
   m = C.readAndCheck( configDir, configFile, configEntries )
   return m

#===========================================================================
def log( config, logFile=None ):
   if not logFile:
      logFile = config.logFile
   
   return util.log.get( "acurite", config.logLevel, logFile )

#===========================================================================



