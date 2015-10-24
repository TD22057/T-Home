T-Home Automation Software
==========================

A collection of scripts and utilities for various home automation projects.

- bin/  Command line tools
- conf/ Sample config files
- init.d/   Init.d style Linux startup scripts
- python/  Main scripting library
- upstart/  Upstart style startup scripts

Currently most of the scripts read data from various sources and
translate the dta into JSON'ed dictionaries which get published to a
ZeroMQ message server.  I'm going to be transitioning this to use MQTT
messages in the near future.


Rainforest Eagle Energy Monitor
-------------------------------

http://rainforestautomation.com/rfa-z109-eagle/

python/tHome/eagle contains code for reading data directly from an
Eagle energy monitor.  Use bin/tHome-eagle.py to start a small web
server and set the address as the "cloud provider" in the Eagle.  The
Eagle will publish energy data to the server which will converts it
into a message and publishes that as a ZeroMQ message.


SMA Solar Inverter
------------------

python/tHome/sma contains code for reading data from an SMA WebConnect
module attached to a SunnyBoy solar inverter.  The Link class is used
for communication but most needs can be satisified by using the report
module which has several report styles (brief to full).

bin/tHome-sma.py is a projess which will poll the inverter at regular
interval while the sun is up, and publish the results as a ZeroMQ
message.

The communication protocol is based on the C code in the
https://sbfspot.codeplex.com/ project.

For a simple example and test, see the scripts in 
python/tHome/sma/test/real

Radio Thermostat
----------------

http://www.radiothermostat.com/

python/tHome/thermostat contains code for polling a radio thermostat
WIFI module and reading the temperature and furnace/AC state.  The
results are published as a ZeroMQ message.

