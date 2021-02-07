#!/usr/bin/python

url="https://dynamodb.eu-central-1.amazonaws.com"
region="eu-central-1"
#tty="/dev/cu.wchusbserial1410"
tty="/dev/ttyUSB0"
therm_rate=120
thermo_name="InsideHall"
state_prefix="."
def_temp = 7 
relay="959BI_1"
relay_on = "0"
relay_off = "1"
relay_cmd = "/usr/local/bin/usbrelay"
