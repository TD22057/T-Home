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
   "Eagle" : [
      # ( name, converter function, default value )
      ( "HttpPort", int, 22042 ),
      ( "LogFile", C.toPath, None ),
      ( "LogLevel", int, 20 ), # INFO
      ],
   }

#===========================================================================
def update( data ):
   C.update( data, sectionDef )
   return data.Eagle
   
#===========================================================================



