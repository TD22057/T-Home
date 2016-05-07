#===========================================================================
#
# SMA WebConnect solar inverter configuration
#
#===========================================================================
# Lat and lon of the installation location used to compute rise/set
# times for the sun.  Time pad is the time to offset from the rise/set
# time in seconds at which to start polling the inverter.
lat = 34.466426
lon = -118.521923
timePad = 600  # 10 minutes before/after sunrise/set

# WebConnect module location.
host = '192.168.1.14'
port = 9522
group = 'USER'
password = '0000'

#===========================================================================
#
# Reporting configuration
#
#===========================================================================
# Polling interval in seconds for each of the reports.  Use zero
# to disable a report.
pollPower = 15
pollEnergy = 600
pollFull = 0

#===========================================================================
#
# MQTT topic names
#
#===========================================================================
# Meter reading topic (reports daily energy total in kWh)
mqttEnergy = 'power/solar/Home/energy'

# Instantaneous power usage topic (reports power usage in W)
mqttPower = 'power/solar/Home/power'

# Detailed data from full report (somewhat slow to run)
mqttFull = 'power/solar/Home/detail'

#===========================================================================
#
# Logging configuration
#
#===========================================================================
logFile = '/var/log/tHome/sma.log'
logLevel = 40

