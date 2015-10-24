#===========================================================================
#
# Reading Message
#
#===========================================================================
from .Base import Base
from . import convert

#==========================================================================
class Reading ( Base ):
   """Reading message

   After construction, will have the following attributes:

      Value            float
      TimeStamp        float (UTC sec past 1-JAN-2000 00:00)
      Type             str

      Time             datetime UTC time stamp
      TimeUnix         float (UTC sec past 1-JAN-1970 00:00)

   Sample:

   <Reading>
     <Value>-123.345</Value>
     <TimeStamp>0x1c531d48</TimeStamp>
     <Type>Summation</Type>
   </Reading>
   """

   # Hex keys turn into floats or ints.  Taken care of automatically
   # in Base.__init__().
   _intHexKeys = []
   _numHexKeys = [ "TimeStamp" ]

   _jsonKeys = [ "Value", "Type" ]
   
   #------------------------------------------------------------------------
   def __init__( self, node ):
      """node == xml ETree node
      """
      assert( node.tag == "Reading" )
      Base.__init__( self, "Reading", node )

      convert.time( self, "Time", "TimeUnix", self.TimeStamp )
      self.Value = float( self.Value )

   #------------------------------------------------------------------------

#==========================================================================
   
      
