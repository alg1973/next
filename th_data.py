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

class th_data:
        def __init__(self):
            self.thermo_name=tconf.thermo_name
            self.minutes=60
            self.db=dyndb.Tempdb(tconf.url,tconf.region)
            
            
        def get_data(self, period=60):
            if period is None or period <=0:
                period = self.minutes
                
            response = self.db.thermo_get_minutes(period,self.thermo_name)
            dates = list()
            temp = list()

            for i in response['Items']:
                dates.append(float(i['GetDate']))
                temp.append(float(i.get('val1', -1)))
            return (dates,temp)

