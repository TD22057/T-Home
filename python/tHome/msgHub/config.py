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
   "MsgHub" : [
      # ( name, converter function, default value )
      ( "Host", str, None ),
      ( "InputPort", int, 22040 ),
      ( "OutputPort", int, 22041 ),
      ( "LogFile", C.toPath, None ),
      ( "LogLevel", int, 20 ), # INFO
      ],
   }

#===========================================================================
def update( data ):
   C.update( data, sectionDef )
   return data.MsgHub
   
#===========================================================================



