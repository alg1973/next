#!/usr/bin/python

url="https://dynamodb.eu-central-1.amazonaws.com"
region="eu-central-1"
#tty="/dev/cu.wchusbserial1410"
tty="/dev/ttyUSB0"
therm_rate=300
thermo_name="InsideHall"
state_prefix="."
log="./therm.log"
def_temp = 5 
relay="959BI_1"
relay_on = "1"
relay_off = "0"
relay_cmd = "/usr/local/bin/usbrelay"
