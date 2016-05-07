#!/bin/bash

# This script configures the eb/ip tables rules to redirect traffic
# from the bridge to a different port on the local machine.  It gets
# run by adding this line to /etc/network/interfaces
#
#    pre-up /home/ted/proj/tHome/bin/acurite-redirect.sh
#

# Redirect traffic on the bridge to port 22041 which must match the port
# specified in tHome/conf/acurite.py.
PORT=22041

# Tell the bridge to push the packet to iptables.
ebtables -t broute -A BROUTING -p IPv4 --ip-protocol 6 --ip-destination-port 80 -j redirect --redirect-target ACCEPT

# Redirect the packet to the other port.
iptables -t nat -A PREROUTING -i br0 -p tcp --dport 80 -j REDIRECT --to-port $PORT
