#===========================================================================
#
# Config file
#
#===========================================================================

__doc__ = """Config file parsing.
"""

from .. import util
from ..util import config as C
from .Thermostat import Thermostat

#===========================================================================

# Config file section name and defaults.
configEntries = [
   # ( name, converter function, default value )
   C.Entry( "logFile", util.path.expand ),
   C.Entry( "logLevel", int, 20 ), # INFO
   C.Entry( "thermostats", list ),
   ]

thermostatEntries = [
   # ( name, converter function, default value )
   C.Entry( "host", str ),
   C.Entry( "label", str ),
   C.Entry( "mqttTempTopic", str ),
   C.Entry( "mqttModeTopic", str ),
   C.Entry( "mqttStateTopic", str ),
   C.Entry( "mqttSetTopic", str ),
   ]

#===========================================================================
def parse( configDir, configFile='thermostat.py' ):
   m = C.readAndCheck( configDir, configFile, configEntries )

   # Replace the thermostat dict inputs with Thermostat objecdts.
   m.thermostats = parseThermostats( m.thermostats )
   
   return m

#===========================================================================
def parseThermostats( entries ):
   assert( len( entries ) > 0 )

   thermostats = []
   for e in entries:
      C.check( e, thermostatEntries )
      thermostats.append( Thermostat( **e ) )

   return thermostats

#===========================================================================
def log( config, logFile=None ):
   if not logFile:
      logFile = config.logFile
   
   return util.log.get( "thermostat", config.logLevel, logFile )

#===========================================================================



