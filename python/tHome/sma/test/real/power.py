#!/usr/bin/env python

import tHome as T

#T.util.log.get( 'sma', 10, 'stdout' )

r = T.sma.report.power( ip="192.168.1.14" )
print "=================="
print r
