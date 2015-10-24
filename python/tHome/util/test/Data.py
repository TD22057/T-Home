
from tHome.util import Data

d = Data( a=1, b="asdf", c=2 )
print d
print "----"

d = Data( a=1, b="asdf", c=[2,3,4] )
print d
print "----"

d = Data( a=1, b="asdf", c={'a':3, 'b':4} )
print d
print "----"

d = Data( a=1, b=[ Data(a=1,b=2) ], c={'a':3, 'b':[1,2,3]} )
print d
print "----"

