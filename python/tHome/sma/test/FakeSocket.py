
class FakeSocket:
   def __init__( self, reply ):
      self.sent = None
      self.reply = reply
      self.closed = False
      
   def send( self, bytes ):
      self.sent = bytes

   def recv( self, bufLen ):
      return self.reply

   def close( self ):
      self.closed = True
      
