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
configEntries = {
   # ( name, converter function, default value )
   C.Entry( "host", str ),
   C.Entry( "port", int, 1883 ),
   C.Entry( "keepAlive", int, 60 ),
   C.Entry( "user", str ),
   C.Entry( "password", str ),
   C.Entry( "ca_certs", list ),
   C.Entry( "certFile", util.path.expand ),
   C.Entry( "keyFile", util.path.expand ),
   }

#===========================================================================
def parse( configDir, configFile='broker.py' ):
   cfg = C.readAndCheck( configDir, configFile, configEntries )

   if cfg.ca_certs:
      for i in range( len( cfg.ca_certs ) ):
         cfg.ca_certs[i] = util.path.expand( cfg.ca_certs[i] )

   return cfg

#===========================================================================



