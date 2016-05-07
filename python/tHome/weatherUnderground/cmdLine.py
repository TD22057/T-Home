#===========================================================================
#
# Command line processing
#
#===========================================================================

import argparse
import numpy as np
from .. import broker
from . import config
from . import start

#===========================================================================

def run( args ):
   """Parse command line arguments to upload weather data.

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
   p.add_argument( "--debug", default=False, action="store_true",
                   help="Debugging - no sending, just print" )
   c = p.parse_args( args[1:] )

   if c.debug:
      c.log = "stdout"

   # Parse the sma and broker config files.
   cfg = config.parse( c.configDir )
   log = config.log( cfg, c.log )

   if c.debug:
      log.setLevel( 10 )

   # Create the MQTT client and connect it to the broker.
   client = broker.connect( c.configDir, log )
   
   # Numpy reports invalid errors when dealing w/ nans which don't
   # matter to this algorithm.
   with np.errstate( invalid='ignore' ):
      start.start( cfg, client, debug=c.debug )

#===========================================================================
