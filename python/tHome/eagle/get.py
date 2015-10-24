from . import config
#from . import convert
#from .DeviceData import DeviceData
#from .DeviceInfo import DeviceInfo
#from .InstantDemand import InstantDemand
#from .Reading import Reading
#from .Total import Total
import xml.etree.ElementTree as ET
import socket

#==========================================================================
def all():
   # Newlines are required 
   xmlCmd = "<LocalCommand>\n<Name>get_device_data</Name>\n" \
            "<MacId>%s</MacId>\n</LocalCommand>\n" % ( config.macAddress )
   xmlData = sendXml( xmlCmd )

   # Add fake wrapper for parsing list of elements
   xmlData = "<root>%s</root>" % xmlData
   root = ET.fromstring( xmlData )

   return DeviceData( root )

#==========================================================================
def device():
   # Newlines are required 
   xmlCmd = "<LocalCommand>\n<Name>list_devices</Name>\n</LocalCommand>\n" 
   xmlData = sendXml( xmlCmd )
   root = ET.fromstring( xmlData )

   return DeviceInfo( root )
   
#==========================================================================
def instant():
   # Newlines are required 
   xmlCmd = "<LocalCommand>\n<Name>get_instantaneous_demand</Name>\n" \
            "<MacId>%s</MacId>\n</LocalCommand>\n" % ( config.macAddress )
   xmlData = sendXml( xmlCmd )
   root = ET.fromstring( xmlData )

   return InstantDemand( root )

#==========================================================================
def history( start ):
   "start == datetime in utc"
   startHex = convert.fromTime( start )
   
   # Newlines are required 
   xmlCmd = "<LocalCommand>\n<Name>get_history_data</Name>\n" \
            "<MacId>%s</MacId>\n<StartTime>%s</StartTime>\n" \
            "</LocalCommand>\n" % ( config.macAddress, startHex )
   xmlData = sendXml( xmlCmd )

   # Add fake wrapper for parsing list of elements
   root = ET.fromstring( xmlData )

   return [ Total( child ) for child in root ]
   
#==========================================================================
def instantHistory( interval ):
   "interval = 'hour', 'day', 'week'"
   assert( interval in [ 'hour', 'day', 'week' ] )

   # Newlines are required 
   xmlCmd = "<LocalCommand>\n<Name>get_demand_values</Name>\n" \
            "<MacId>%s</MacId>\n</LocalCommand>\n" % ( config.macAddress )
   xmlData = sendXml( xmlCmd )

   # Add fake wrapper for parsing list of elements
   xmlData = "<root>%s</root>" % xmlData
   root = ET.fromstring( xmlData )

   return Reading.xmlToList( root )
   
#==========================================================================
def totalHistory( interval ):
   "interval = 'day', 'week', 'month', 'year'"
   assert( interval in [ 'day', 'week', 'month', 'year' ] )
   
   # Newlines are required 
   xmlCmd = "<LocalCommand>\n<Name>get_summation_values</Name>\n" \
            "<MacId>%s</MacId>\n</LocalCommand>\n" % ( config.macAddress )
   xmlData = sendXml( xmlCmd )

   # Add fake wrapper for parsing list of elements
   xmlData = "<root>%s</root>" % xmlData
   root = ET.fromstring( xmlData )
   
   return Reading.xmlToList( root )

#==========================================================================
def sendXml( xmlCmd ):
   sock = socket.create_connection( ( config.host, config.port ) )
   try:
      sock.send( xmlCmd )

      buf = ""
      while True:
         s = sock.recv( 1024 )
         if not s:
            break

         buf += s
   finally:
      sock.close()

   return buf

#==========================================================================
