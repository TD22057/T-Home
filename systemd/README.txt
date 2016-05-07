Systemd notes:

Install in:
/etc/systemd/system

probably use sym links there.

Then run:
   systemctl start [name]

If there are errors, run:

   systemctl status [name]

After editing a service file, run:

   systemctl daemon-reload [name]


To enable auto-start at boot time:

   systemctl enable [name].service
