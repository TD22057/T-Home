#=============================================================================
import StringIO

#=============================================================================
class Data:
   def __init__( self, dict=None, **kwargs ):
      if dict:
         self.__dict__.update( dict )
      if kwargs:
         self.__dict__.update( kwargs )
      
   #--------------------------------------------------------------------------
   def keys( self ):
      return self.__dict__.keys()
   
   #--------------------------------------------------------------------------
   def update( self, rhs ):
      return self.__dict__.update( rhs.__dict__ )
   
   #--------------------------------------------------------------------------
   def __setitem__( self, key, value ):
      self.__dict__[key] = value
      
   #--------------------------------------------------------------------------
   def __getitem__( self, key ):
      return self.__dict__[key]
   
   #--------------------------------------------------------------------------
   def __str__( self ):
      out = StringIO.StringIO()
      self._formatValue( self, out, 3 )
      return out.getvalue()

   #--------------------------------------------------------------------------
   def __repr__( self ):
      return self.__str__()
      
   #--------------------------------------------------------------------------
   def _formatValue( self, value, out, indent ):
      if isinstance( value, Data ):
         out.write( "%s(\n" % self.__class__.__name__ )
         for k, v in sorted( value.__dict__.iteritems() ):
            if k[0] == "_":
               continue
            
            out.write( "%*s%s" % ( indent, '', k ) )
            out.write( " = " )
            self._formatValue( v, out, indent+3 )
            out.write( ",\n" )

         out.write( "%*s)" % ( indent, '' ) )
         
      elif isinstance( value, dict ):
         out.write( "{\n" )
         for k, v in sorted( value.iteritems() ):
            if k[0] == "_":
               continue
            
            out.write( "%*s" % ( indent, '' ) )
            self._formatValue( k, out, 0 )
            out.write( " : " )
            self._formatValue( v, out, indent+3 )
            out.write( ",\n" )

         out.write( "%*s}" % ( indent, '' ) )

      elif isinstance( value, list ):
         out.write( "[\n" )
         for i in value:
            out.write( "%*s" % ( indent, '' ) )
            self._formatValue( i, out, indent+3 )
            out.write( ",\n" )

         out.write( "%*s]" % ( indent, '' ) )
            
      elif isinstance( value, str ):
         out.write( "'%s'" % ( value ) )
         
      else:
         out.write( "%s" % ( value ) )
            
            
            
      
#=============================================================================
