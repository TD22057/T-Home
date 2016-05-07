#===========================================================================
#
# RainForest Eagle Electric meter reading package
#
#===========================================================================

__doc__ = """RainForest Eagle electric meter reader.

This package implements a web server which the RainForest Eagle can use as a cloud service.  The Eagle will post data to the this module which parses the XML messages and sends them out as ZeroMQ messages (usually to a tHome.msgHub).

Logging object name: tHome.eagle
"""

#===========================================================================


#===========================================================================

from . import config
from .connect import connect

#===========================================================================
