#===========================================================================
#
# msgHub package
#
#===========================================================================

__doc__ = """Zero-MQ Message Hub

The msgHub is a pub/sub forwarder.  All of the various data producers
send messages to the msgHub as a single point of contact for the
producers.  Consumers of the messages read from the hub as a single
point of contact for the consumers.

Logging object name: tHome.msgHub
"""

#===========================================================================


#===========================================================================

from . import cmdLine
from . import config
from .start import start

#===========================================================================

