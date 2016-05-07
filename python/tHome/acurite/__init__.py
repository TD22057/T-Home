#===========================================================================
#
# Acurite weather station package.
#
#===========================================================================

__doc__ = """T-Home Acurite weather station package.

Used to intercept Acurite post commands from an Acurite bridge being
posted to the Acurite web sites.  The bridge reads radio traffic from
the sensors and posts them.

This package assumes the code is run on a system in-line with the
bridge.  See: http://www.bobshome.net/weather/ for details.

Designed for use w/ a Raspberry Pi.  Use a USB network adaptor and
plug the bridge into the adaptor.  Run the code on the pi with the USB
network adaptor set up as a bridge to the regular network.

On the PI, install bridge and TCP monitoring utilities:

   apt-get install bridge-utils tcpdump tcpflow 

Then edit /etc/network/interfaces to configure the USB network as a
bridge to the main network.

--------------
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp

auto eth1 br0
iface br0 inet dhcp
iface eth1 inet manual

bridge_ports eth0 eth1
--------------

The restart the network:

   sudo service networking restart

To access the data, use tcpflow (see bin/acurite-read.sh for this
script) to intercept data from the USB link and pass it to the script.

--------------
#!/bin/sh

SCRIPT=$HOME/tHome/bin/acurite-send.py
LOG=/var/log/tHome/acurite-send.log

(/usr/bin/tcpflow -c -i eth1 -s tcp dst port 80 | $SCRIPT) 2>> $LOG &
--------------

"""

#===========================================================================
from . import cmdLine
from . import config
from .decode import decode
from . import mqtt
from .Sensor import Sensor

#===========================================================================


