SCRIPT=tHome-thermostat

sudo cp $SCRIPT /etc/init.d/
cd /etc/init.d/
ll $SCRIPT
sudo chmod 755 $SCRIPT
sudo update-rc.d $SCRIPT defaults
sudo update-rc.d $SCRIPT enable
sudo service $SCRIPT start
