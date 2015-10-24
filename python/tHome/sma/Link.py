#===========================================================================
#
# Primary SMA API.
#
#===========================================================================

import socket
from .. import util
from . import Auth
from . import Reply
from . import Request

#==============================================================================
class Link:
   """SMA WebConnection link

   Units: Watt, Watt-hours, C, seconds

   l = Link( '192.168.1.14' )
   print l.acTotalEnergy()

   See also: report for common requests.
   """
   def __init__( self, ip, port=9522, group="USER", password="0000",
                 connect=True, timeout=120, decode=True, raw=False ):
      assert( group == "USER" or group == "INSTALLER" )
      
      self.ip = ip
      self.port = port
      self.group = group
      self.password = password
      self.timeout = timeout
      self.decode = decode
      self.raw = raw

      self.socket = None
      if connect:
         self.open()

   #---------------------------------------------------------------------------
   def info( self ):
      p = Request.Data( command=0x58000200, first=0x00821E00, last=0x008220FF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [ 
         Reply.StringItem( "name", 40, timeVar="timeWake" ),
         Reply.AttrItem( "type", 40 ),
         Reply.AttrItem( "model", 40 ),
         ] )
      return self._return( bytes, decoder )
      
   #---------------------------------------------------------------------------
   def status( self ):
      p = Request.Data( command=0x51800200, first=0x00214800, last=0x002148FF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.AttrItem( "status", 32, timeVar="time" ),
         ] )
      return self._return( bytes, decoder )
   
   #---------------------------------------------------------------------------
   def gridRelayStatus( self ):
      p = Request.Data( command=0x51800200, first=0x00416400, last=0x004164FF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.AttrItem( "gridStatus", 32, timeVar="timeOff" ),
         ] )
      return self._return( bytes, decoder )

   #---------------------------------------------------------------------------
   def temperature( self ):
      """Return the inverter temp in deg C (or 0 if unavailable)."""
      p = Request.Data( command=0x52000200, first=0x00237700, last=0x002377FF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.I32Item( "temperature", 16, mult=0.01 ),
         ] )
      return self._return( bytes, decoder )
   
   #---------------------------------------------------------------------------
   def version( self ):
      """Return the inverter software version string."""
      p = Request.Data( command=0x58000200, first=0x00823400, last=0x008234FF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.VersionItem( "version" ),
         ] )
      return self._return( bytes, decoder )
   
   #---------------------------------------------------------------------------
   def acTotalEnergy( self ):
      p = Request.Data( command=0x54000200, first=0x00260100, last=0x002622FF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.I64Item( "totalEnergy", 16, mult=1.0, timeVar="timeLast" ),
         Reply.I64Item( "dailyEnergy", 16, mult=1.0 ),
         ] )
      return self._return( bytes, decoder )

   #---------------------------------------------------------------------------
   def acTotalPower( self ):
      p = Request.Data( command=0x51000200, first=0x00263F00, last=0x00263FFF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.I32Item( "acPower", 28, mult=1.0, timeVar="timeOff" ),
         ] )
      return self._return( bytes, decoder )
      
   #---------------------------------------------------------------------------
   def acPower( self ):
      p = Request.Data( command=0x51000200, first=0x00464000, last=0x004642FF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.I32Item( "acPower1", 28, mult=1.0, timeVar="timeOff" ),
         Reply.I32Item( "acPower2", 28, mult=1.0 ),
         Reply.I32Item( "acPower3", 28, mult=1.0 ),
         ] )
      return self._return( bytes, decoder )

   #---------------------------------------------------------------------------
   def acMaxPower( self ):
      p = Request.Data( command=0x51000200, first=0x00411E00, last=0x004120FF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.U32Item( "acMaxPower1", 28, mult=1.0, timeVar="time" ),
         Reply.U32Item( "acMaxPower2", 28, mult=1.0 ),
         Reply.U32Item( "acMaxPower3", 28, mult=1.0 ),
         ] )
      return self._return( bytes, decoder )

   #---------------------------------------------------------------------------
   def operationTime( self ):
      p = Request.Data( command=0x54000200, first=0x00462E00, last=0x00462FFF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.I64Item( "operationTime", 16, mult=1.0, timeVar="timeLast" ),
         Reply.I64Item( "feedTime", 16, mult=1.0 ),
         ] )
      return self._return( bytes, decoder )

   #---------------------------------------------------------------------------
   def dcPower( self ):
      p = Request.Data( command=0x53800200, first=0x00251E00, last=0x00251EFF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.I32Item( "dcPower1", 28, mult=1.0, timeVar="timeOff" ),
         Reply.I32Item( "dcPower2", 28, mult=1.0 ),
         ] )
      return self._return( bytes, decoder )

   #---------------------------------------------------------------------------
   def dcVoltage( self ):
      p = Request.Data( command=0x53800200, first=0x00451F00, last=0x004521FF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.I32Item( "dcVoltage1", 28, mult=0.01, timeVar="timeOff" ),
         Reply.I32Item( "dcVoltage2", 28, mult=0.01 ),
         Reply.I32Item( "dcCurrent1", 28, mult=0.001 ),
         Reply.I32Item( "dcCurrent2", 28, mult=0.001 ),
         ] )
      return self._return( bytes, decoder )

   #---------------------------------------------------------------------------
   def acVoltage( self ):
      p = Request.Data( command=0x51000200, first=0x00464800, last=0x004652FF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.U32Item( "acVoltage1", 28, mult=0.01, timeVar="timeOff" ),
         Reply.U32Item( "acVoltage2", 28, mult=0.01 ),
         Reply.U32Item( "acVoltage3", 28, mult=0.01 ),
         Reply.U32Item( "acGridVoltage", 28, mult=0.01 ),
         Reply.U32Item( "unknown1", 28, mult=0.01 ),
         Reply.U32Item( "unknown2", 28, mult=0.01 ),
         Reply.U32Item( "acCurrent1", 28, mult=0.001 ),
         Reply.U32Item( "acCurrent2", 28, mult=0.001 ),
         Reply.U32Item( "acCurrent3", 28, mult=0.001 ),
         ] )
      return self._return( bytes, decoder )

   #---------------------------------------------------------------------------
   def gridFrequency( self ):
      p = Request.Data( command=0x51000200, first=0x00465700, last=0x004657FF )
      bytes = p.send( self.socket )
      decoder = Reply.Value( [
         Reply.U32Item( "frequency", 28, mult=0.01, timeVar="timeOff" ),
         ] )
      return self._return( bytes, decoder )

   #---------------------------------------------------------------------------
   def __del__( self ):
      self.close()
      
   #---------------------------------------------------------------------------
   def open( self ):
      if self.socket:
         return

      self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
      self.socket.settimeout( self.timeout )
      try:
         self.socket.connect( ( self.ip, self.port ) )

         p = Auth.LogOn( self.group, self.password )
         p.send( self.socket )
      except:
         if self.socket:
            self.socket.close()
            
         self.socket = None
         raise

   #---------------------------------------------------------------------------
   def close( self ):
      if not self.socket:
         return

      p = Auth.LogOff()
      try:
         p.send( self.socket )
      finally:
         self.socket.close()
         self.socket = None

   #---------------------------------------------------------------------------
   def __enter__( self ):
      return self

   #---------------------------------------------------------------------------
   def __exit__( self, type, value, traceback ):
      self.close()

   #---------------------------------------------------------------------------
   def _return( self, bytes, decoder ):
      if self.decode:
         return decoder.decode( bytes, self.raw )
      else:
         return ( bytes, decoder )
   
#==============================================================================
