#!/usr/bin/python 

import sys
import time
import dyndb
import tconf
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

thermo_name=tconf.thermo_name
minutes=60
frm = 'table'

if len(sys.argv)==2:
	minutes=int(sys.argv[1])

elif len(sys.argv)==3:
	minutes=int(sys.argv[1])
        frm=sys.argv[2]


db=dyndb.Tempdb(tconf.url,tconf.region)
response = db.thermo_get_minutes(minutes,thermo_name)

if frm == 'data':
    for i in response['Items']:
        print("{1} {0}".format(float(i['GetDate']),float(i.get('val1', -1))))
else:    
    for i in response['Items']:
        print(time.ctime(float(i['GetDate'])),'temp1',float(i.get('val1', -1)), 'temp2', float(i.get('val2', -1)),
              'target temp',int(i.get('target',-1)),'heating cmd',int(i.get('heating',-1)), 
              'boiler state', int(i.get('boiler_state',-1)))


