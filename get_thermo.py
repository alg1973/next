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


if len(sys.argv)==2:
	minutes=int(sys.argv[1])
        thermo_name=tconf.thermo_name
elif len(sys.argv)==3:
	minutes=int(sys.argv[1])
        thermo_name=sys.argv[2]
else:
	minutes=60
        thermo_name=tconf.thermo_name

db=dyndb.Tempdb(tconf.url,tconf.region)
response = db.thermo_get_minutes(minutes,thermo_name)


for i in response['Items']:
    print(time.ctime(float(i['GetDate'])),'temp',float(i['val']), 'hum', float(i['hum']),
			int(i.get('target',-1)),int(i.get('heating',-1)))


