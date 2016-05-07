T-Home Automation Software
==========================

A collection of scripts and utilities for various home automation projects.

- bin/  Command line tools
- conf/ Sample config files
- init.d/   Init.d style Linux start up scripts
- python/  Main scripting library
- systemd/  Systemd (latest Raspian) start up scripts
- upstart/  Upstart (Ubuntu 14.04) style start up scripts

Currently most of the scripts read data from various sources and
translate the data into JSON'ed dictionaries which get published to a
MQTT message broker.  


Acurite Weather Station
-----------------------

python/tHome/acurite contains code for decoding Acurite internet
Bridge traffic.  This assumes the Acurite Bridge is connected to a
network USB dongle on a Raspberry Pi.  It uses iptables and ebtables
to redirect the bridge traffic (which normally posts data to Acurite's
web servers) to the script bin/tHome-acurite.py.  That script
simulates the response from Acurite's servers, decodes the data, and
translates them into MQTT messages.  This can also be used with
tcpflow to decode data as it's being sent to Acurite instead of
redirecting it.

Radio Thermostat
----------------

http://www.radiothermostat.com/

python/tHome/thermostat contains code for polling a radio thermostat
WIFI module and reading the temperature and furnace/AC state.  The
results are published as MQTT messages.


Rainforest Eagle Energy Monitor
-------------------------------

http://rainforestautomation.com/rfa-z109-eagle/

python/tHome/eagle contains code for reading data directly from an
Eagle energy monitor.  Use bin/tHome-eagle.py to start a small web
server and set the address as the "cloud provider" in the Eagle.  The
Eagle will publish energy data to the server which will converts it
into a message and publishes that as a MQTT messages.


SMA Solar Inverter
------------------

python/tHome/sma contains code for reading data from an SMA WebConnect
module attached to a SunnyBoy solar inverter.  The Link class is used
for communication but most needs can be satisfied by using the report
module which has several report styles (brief to full).

bin/tHome-sma.py is a process which will poll the inverter at regular
interval while the sun is up, and publish the results as MQTT messages.

The communication protocol is based on the C code in the
https://sbfspot.codeplex.com/ project.


Weather Underground
-------------------

python/tHome/weatherUnderground contains code that subscribes to
messages produced by the Acurite Bridge module and uploads that
information to Weather Underground.  It will upload data at a user
specified interval and uses a sliding window average of the sensor
data over that upload interval to smooth the sensors before uploading
them (including correctly averaging wind direction data).

Use bin/tHome-wug.py to start this process.


