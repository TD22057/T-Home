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
   C.Entry( "uploadUrl", str ),
   C.Entry( "id", str ),
   C.Entry( "password", str ),
   C.Entry( "poll", int, 120 ),
   C.Entry( "maxRate", int, 10 ),
   C.Entry( "digits", int, 2 ),
   C.Entry( "mqttWind", str, None ),
   C.Entry( "mqttTemp", list, [] ),
   C.Entry( "mqttRain", str, None ),
   C.Entry( "mqttBarometer", str, None ),
   C.Entry( "mqttHumidity", str, None ),
   C.Entry( "logFile", util.path.expand ),
   C.Entry( "logLevel", int, 20 ), # INFO
   ]

#===========================================================================
def parse( configDir, configFile='weatherUnderground.py' ):
   return C.readAndCheck( configDir, configFile, configEntries )

#===========================================================================
def log( config, logFile=None ):
   if not logFile:
      logFile = config.logFile
   
   return util.log.get( "weatherUnderground", config.logLevel, logFile )

#===========================================================================



