#===========================================================================
#
# Poll
#
#===========================================================================

import select
import errno

#===========================================================================
class Poll:
   """: Posix poll manager.

   This classes manages the polling behavior for normal posix (non-gui)
   network code.  See the Python select module or UNIX poll
   documentation for details.

   Server and Link objects are added to the Poll and it will manage
   the I/O calls for each of them.  Instead of having a poll() method
   like the Python module, this class has a select() method to kee the
   API identical to the mpy.net.Select class.
   
   = EXAMPLE

   # MPY_NO_TEST
   # # Setup server and/or links here.
   #
   # # Create the select and add the servers/links to it.
   # mgr = Poll()
   # for c in clients:
   #    mgr.add( c )
   #
   # # Loop to process.
   # while True:
   #    mgr.select()
   """
   #-----------------------------------------------------------------------
   def __init__( self ):
      """: Constructor."""
      # Create the polling object.
      self.poll = select.poll()

      # Key is a file descripter for the socket of the object being
      # watched.  Value is a Link or Server object for that socket.
      self.clients = {}

      # Bit flags to watch for when registering a socket for read or
      # read/write.
      self.READ = select.POLLIN | select.POLLPRI | select.POLLHUP | \
                  select.POLLERR
      self.READ_WRITE = self.READ | select.POLLOUT

      # Bit flags reported for events.
      self.EVENT_READ = select.POLLIN | select.POLLPRI
      self.EVENT_WRITE = select.POLLOUT
      self.EVENT_CLOSE = select.POLLHUP
      self.EVENT_ERROR = select.POLLERR

      # NOTE: These bit flags were originally class variables
      # (accessed via Poll.READ, etc) but a weird race condition in
      # Python multi-threaded code (mpy.parallel) would sometimes
      # throw an exception saying Poll was None.  No idea why that
      # could happen but making these member variables seems to fix
      # the problem.

   #-----------------------------------------------------------------------
   def active( self ):
      """: Return the number of sockets being watched.

      Used for single point connections to automatically exit a select
      function when connections close.

      = EXAMPLE
      
      # MPY_NO_TEST
      # select = Poll()
      # select.add( client1 )
      # select.add( client12 )
      #
      # while select.active():
      #    select.select()
      """
      return len( self.clients )
      
   #-----------------------------------------------------------------------
   def add( self, obj ):
      """: Add a link or server to the select.

      Call obj.close() to remove the object.
      
      = INPUT VARIABLES
      - obj   The Link or Server object to add to the select.
      """
      # All sockets are checked for reading since a read of 0 means a
      # dropped connection.  Errors are also checked even though they
      # rarely occur.  Sockets for writing is handled in the
      # clientCanWrite() callback that is triggered through the
      # watcher mechanism below.
      self.poll.register( obj.fileno, self.READ )
      
      # Save the object for later use.
      self.clients[ obj.fileno ] = obj
      
      # Tell the object it's part of this Poll.  This allows it to
      # close the connection and tell the Poll about it.  In
      # addition, the client can notify us if there is data to write
      # or not.
      obj.sigClosing.connect( self.closeLink )
      obj.sigCanWrite.connect( self.linkCanWrite )

   #-----------------------------------------------------------------------
   def remove( self, obj ):
      """: Remove an object from the select.

      Normally this is called by the object being removed when
      obj.close() is called (i.e. this should not normally be called).

      = INPUT VARIABLES
      - obj           The object that is closing.  This should be the
                      same object that was passed to add().
      """
      # Remove the object from our structures.
      self.poll.unregister( obj.fileno )
      del self.clients[ obj.fileno ]

      # Tell the object to remove ourselves from it's watch list.
      obj.sigClosing.disconnect( self.closeLink )
      obj.sigCanWrite.disconnect( self.linkCanWrite )

   #-----------------------------------------------------------------------
   def closeAll( self ):
      """: Close all clients attached to the select.

      This will close any Link and Server objects that are part of
      the select.
      """
      # As we close clients, they will notify the select to remove
      # themselves.  So make a copy of the dict value list list
      # containing all the objects so we're not modifying the client
      # dictionary as we loop over it.
      clients = self.clients.values()[:]
      for c in clients:
         c.close()

   #-----------------------------------------------------------------------
   def select( self, timeOut=None ):
      """: Watch the sockets.

      This will call poll.poll() (normal posix poll) and process the
      results when it returns.  All the clients and servers in the
      poll (see the add() method) are checked for reading or errors.
      Any client that returns True when client.canWrite() is called
      will be checked for writing.
      
      If a client has an error, then client.close() is called.  If a
      client can read, then client.read() is called.  If a client can
      write, then client.write() is called.

      See the class documentation for an example.

      = INPUT VARIABLES
      - timeOut   Optional floating point time out for the select call
                  in seconds.  See select.select for more information.
      """
      timeOut_msec = None if timeOut is None else 1000*timeOut

      while True:
         try:
            # Returns tuple (fileDescriptor, bitFlag) of the files
            # that can act.
            events = self.poll.poll( timeOut_msec )
         except select.error, v:
            # Not sure why, but sometimes with a timeout value, you can
            # get an "interrupted system call" error thrown.  Web
            # searches indicate this isn't really an error and should be
            # ignored so test for it here.
            if v[0] != errno.EINTR:
               raise
         else:
            break

      for fd, flag in events:
         # Find the object for this file descriptor.  Certain
         # multi-threaded test cases seem to have a problem with the
         # clientClosing() method not being called (which unregisters
         # the fd) so handle that with a None return here.
         obj = self.clients.get( fd, None )
         if obj is None:
            continue

         # Object has data to read.  If an error occurred during the
         # read, clear the flag so we don't try to do anything else.
         if flag & self.EVENT_READ:
            if obj.readFromSocket() == -1:
               flag = 0

         # Object can write data.
         if flag & self.EVENT_WRITE:
            obj.writeToSocket()

         # Test for errors or closing connections.  Only call close once.
         
         # Connection going down.  
         if flag & self.EVENT_CLOSE:
            obj.close()

         # Error - close the connection - use else here  
         elif flag & self.EVENT_ERROR:
            obj.close()

   #-----------------------------------------------------------------------
   def linkCanWrite( self, obj, writeActive ):
      # Writing should be active.
      if writeActive:
         # Add the socket if it's not already in the write list.
         self.poll.modify( obj.fileno, self.READ_WRITE )

      # Writing should not be active:
      else:
         # Remove the socket if it's in the write list.
         self.poll.modify( obj.fileno, self.READ )
      
   #-----------------------------------------------------------------------
   def closeLink( self, obj ):
      self.remove( obj )

   #-----------------------------------------------------------------------
   
#===========================================================================
