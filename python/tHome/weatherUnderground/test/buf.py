import numpy as np
import warnings
import tHome.weatherUnderground.start as S

buf = S.CircularTimeBuf( 60, 10 )

print "================="
print "Empty"
print "================="
print "Min/Max: %s / %s Avg: %s" % ( buf.min(), buf.max(), buf.mean() )

print "================="
buf.append( 10, 1 )
print buf.v
print "Min/Max: %s / %s Avg: %s" % ( buf.min(), buf.max(), buf.mean() )
print

buf.append( 20, 2 )
print buf.v
print "Min/Max: %s / %s Avg: %s" % ( buf.min(), buf.max(), buf.mean() )
print

buf.append( 30, 3 )
print buf.v
print "Min/Max: %s / %s Avg: %s" % ( buf.min(), buf.max(), buf.mean() )
print

buf.append( 40, 4 )
print buf.v
print "Min/Max: %s / %s Avg: %s" % ( buf.min(), buf.max(), buf.mean() )
print

buf.append( 50, 5 )
print buf.v
print "Min/Max: %s / %s Avg: %s" % ( buf.min(), buf.max(), buf.mean() )
print

buf.append( 60, 6 )
print buf.v
print "Min/Max: %s / %s Avg: %s" % ( buf.min(), buf.max(), buf.mean() )
print

buf.append( 70, 7 )
print buf.v
print "Min/Max: %s / %s Avg: %s" % ( buf.min(), buf.max(), buf.mean() )
print
print "================="

buf.append( 120, 12 )
print buf.v
print "Min/Max: %s / %s Avg: %s" % ( buf.min(), buf.max(), buf.mean() )

print "================="
buf.append( 130, 13 )
buf.append( 140, 14 )
buf.append( 150, 15 )
buf.append( 160, 16 )
buf.append( 170, 17 )
print buf.v
print
print "Update to t=200"
print "Min/Max: %s / %s Avg: %s" % ( buf.min(200), buf.max(200), buf.mean(200) )
print buf.v

print "================="
print "Update to t=500"
buf.updateTo( 500 )
print buf.v

print "Min:",buf.min( 500 )

