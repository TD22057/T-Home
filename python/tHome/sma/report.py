#===========================================================================
#
# Report functions
#
#===========================================================================
import time
from ..util import Data
from .Link import Link

#===========================================================================
def power( *args, **kwargs ):
   """Return instantaneous AC and DC power generation.

   Inputs are the same as Link() constructor:

   obj = report.instant( '192.168.1.15' )
   print obj
   """
   with Link( *args, **kwargs ) as link:
      link.decode = False
      link.raw = False
      dcBytes, dc = link.dcPower()
      acBytes, ac = link.acTotalPower()

   now = time.time()
   obj = dc.decode( dcBytes )
   obj.update( ac.decode( acBytes ) )

   obj.time = now
   obj.dcPower = obj.dcPower1 + obj.dcPower2
   return obj

#===========================================================================
def energy( *args, **kwargs ):
   """Return instantaneous power and total energy status.

   Get instantaneous AC and DC power generation and energy created for
   the day.

   Inputs are the same as Link() constructor:

   obj = report.energy( '192.168.1.15' )
   print obj
   """
   with Link( *args, **kwargs ) as link:
      link.decode = False
      dcBytes, dc = link.dcPower()
      acBytes, ac = link.acTotalPower()
      totBytes, total = link.acTotalEnergy()
      
   now = time.time()
   obj = dc.decode( dcBytes )
   obj.update( ac.decode( acBytes ) )
   obj.update( total.decode( totBytes ) )

   obj.time = now
   obj.dcPower = obj.dcPower1 + obj.dcPower2
   return obj
   
#===========================================================================
def full( *args, **kwargs ):
   """Return all possible fields.
   
   Inputs are the same as Link() constructor:

   obj = report.full( '192.168.1.15' )
   print obj
   """
   funcs = [
      Link.info,
      Link.status,
      Link.gridRelayStatus,
      Link.temperature,
      Link.version,
      Link.acTotalEnergy,
      Link.acTotalPower,
      Link.acPower, 
      Link.acMaxPower,
      Link.operationTime,
      Link.dcPower, 
      Link.dcVoltage,
      Link.acVoltage,
      Link.gridFrequency,
      ]

   with Link( *args, **kwargs ) as link:
      link.decode = False
      results = [ f( link ) for f in funcs ]

   now = time.time()
   obj = Data()
   for bytes, decoder in results:
      obj.update( decoder.decode( bytes ) )

   obj.time = now
   obj.dcPower = obj.dcPower1 + obj.dcPower2
   return obj

#===========================================================================
