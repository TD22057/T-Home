#===========================================================================
#
# Config file
#
#===========================================================================

__doc__ = """Config file parsing.
"""

import re
from .. import config as C
from .Thermostat import Thermostat

#===========================================================================

# Config file section name and defaults.
sectionDef = {
   "Thermostat" : [
      # ( name, converter function, default value )
      ( "PollTime", float, 60 ),
      ( "LogFile", C.toPath, None ),
      ( "LogLevel", int, 20 ), # INFO
      ],
   }

#===========================================================================
def update( data ):
   C.update( data, sectionDef )

   pat = re.compile( r"Thermostat_(\d+)" )

   mdata = data.Thermostat
   mdata.thermostats = []
   
   for s in data._config.sections():
      m = pat.match( s )
      if m:
         t = Thermostat( data._config.get( s, "Label" ),
                         data._config.get( s, "IP" ),
                         data._config.get( s, "Room" ) )
         mdata.thermostats.append( t )
         
   return mdata
   
#===========================================================================



