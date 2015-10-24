#===========================================================================
#
# RainForest Eagle XML messages
#
#===========================================================================

__doc__ = """Decodes Eagle XML messages.

One class per message type.  Use the eagle.parse() function to do the
conversions.
"""

#===========================================================================

from . import convert
from .Base import Base
from .BlockPriceDetail import BlockPriceDetail
from .CurrentSummation import CurrentSummation
from .DeviceInfo import DeviceInfo
from .FastPollStatus import FastPollStatus
from .InstantaneousDemand import InstantaneousDemand
from .MessageCluster import MessageCluster
from .MeterInfo import MeterInfo
from .NetworkInfo import NetworkInfo
from .PriceCluster import PriceCluster
from .Reading import Reading
from .ScheduleInfo import ScheduleInfo
from .TimeCluster import TimeCluster

#===========================================================================

# Map XML names to class names.
tagMap = {
   "BlockPriceDetail" : BlockPriceDetail,
   "CurrentSummation" : CurrentSummation, # socket API
   "CurrentSummationDelivered" : CurrentSummation, # cloud API
   "DeviceInfo" : DeviceInfo,
   "FastPollStatus" : FastPollStatus,
   "InstantaneousDemand" : InstantaneousDemand,
   "MessageCluster" : MessageCluster,
   "MeterInfo" : MeterInfo,
   "NetworkInfo" : NetworkInfo,
   "PriceCluster" : PriceCluster,
   "Reading" : Reading,
   "ScheduleInfo" : ScheduleInfo,
   "TimeCluster" : TimeCluster,
   }

#===========================================================================
