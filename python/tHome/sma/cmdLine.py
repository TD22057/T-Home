#===========================================================================
#
# Command line processing
#
#===========================================================================

import argparse
from .. import config as C
from .. import msgHub
from .. import util
from . import config
from . import start

#===========================================================================

def run( args ):
   """Parse command line arguments to poll the inverter.

   = INPUTS
   - args   [str]: List of command line arguments.  [0] should be the
            program name.
   """
   p = argparse.ArgumentParser( prog=args[0],
                                description="SMA inverter reader" )
   p.add_argument( "-c", "--configDir", metavar="configDir",
                   default="/var/config/tHome",
                   help="T-Home configuration directory." )
   p.add_argument( "-l", "--log", metavar="logFile",
                   default=None, help="Logging file to use.  Input 'stdout' "
                   "to log to the screen." )
   c = p.parse_args( args[1:] )

   # Parse all the config files and extract the MsgHub data.
   data = C.parse( c.configDir )
   cfg = config.update( data )
   hub = msgHub.config.update( data )

   # Override the log file.
   if c.log:
      cfg.LogFile = C.toPath( c.log )

   if cfg.LogFile:
      log = util.log.get( "sma" )
      log.writeTo( cfg.LogFile )
      log.setLevel( cfg.LogLevel )

   start.start( cfg, hub )


#===========================================================================
