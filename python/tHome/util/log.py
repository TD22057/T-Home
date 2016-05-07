#=============================================================================
#
# Logging utilities
#
#=============================================================================
import logging
import logging.handlers
import platform
import sys
import types
from .Error import Error
from . import path

#=============================================================================
_logs = {}

#=============================================================================
def get( name, level=None, output=None ):
   """ TODO: doc
   """
   log = _logs.get( name, None )
   if not log:
      log = create( name )

   if level is not None:
      log.setLevel( level )

   if output is not None:
      writeTo( log, output )

   return log
   
#=============================================================================
def create( name, level=logging.ERROR ):
   """ Create a logging object for the package name.

   The full logging name will be 'tHome.NAME'.
   """
   log = logging.getLogger( 'tHome.%s' % name )
   log.setLevel( level )

   handler = logging.NullHandler()
   handler.setFormatter( _formatter() )
   log.addHandler( handler )

   # Monkey patch a method onto the log class.
   log.writeTo = types.MethodType( writeTo, log )

   # Save a handle to the log.
   _logs[name] = log
   return log
   
#=============================================================================
def writeTo( log, fileName ):
   """ TODO: doc
   """
   if fileName == "stdout":
      handler = logging.StreamHandler( sys.stdout )
   else:
      try:
         path.makeDirs( fileName )

         # Use the watcher on linux so that logrotate will work
         # properly.  It will close and reopen the log file if the OS
         # moves it.  Not supported on windows.
         if platform.system() == "Windows":
            handler = logging.FileHandler( fileName )
         else:
            handler = logging.handlers.WatchedFileHandler( fileName )
            
      except ( Error, IOError ) as e:
         msg = "Error trying to open the log file '%s' for writing." % fileName 
         Error.raiseException( e, msg )

   handler.setFormatter( _formatter() )
   log.addHandler( handler )

#=============================================================================
def _formatter():
   return logging.Formatter( '%(asctime)s : %(levelname)s: %(message)s' )
   
#=============================================================================
