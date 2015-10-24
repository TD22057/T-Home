#===========================================================================
#
# Config file
#
#===========================================================================

__doc__ = """Config file parsing.
"""
from .. import config as C

#===========================================================================

# Config file section name and defaults.
sectionDef = {
   "SMAInverter" : [
      # ( name, converter function, default value )
      ( "Label", str, "Solar Inverter" ),
      ( "IP", str, None ),
      ( "Port", int, 9522 ),
      ( "Group", str, "USER" ),
      ( "Password", str, "0000" ),
      ( "LogFile", C.toPath, None ),
      ( "LogLevel", int, 30 ),
      ( "PollPower", int, 10 ),
      ( "PollEnergy", int, 600 ), # 10 minutes
      ( "PollFull", int, 0 ), # disabled
      ( "Lat", float, None ), 
      ( "Lon", float, None ),
      ( "TimePad", float, 600 ), # 10 minutes
      ],
   }

#===========================================================================
def update( data ):
   C.update( data, sectionDef )
   return data.SMAInverter
   
#===========================================================================



