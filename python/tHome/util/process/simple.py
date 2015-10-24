
#=============================================================================

import subprocess

#=============================================================================

def simple( cmd, cwd=None ):
   """Runs a command and returns stdout and stderr mixed together.

   Throws an Exception w/ the output if it fails.
   """
   # Set stderr to also send output to stdout (i.e. combine them).
   p = subprocess.Popen( cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT )
   ( stdout, stderr ) = p.communicate()
   if p.returncode:
      raise Exception( stdout )

   return stdout

#=============================================================================
