#!/usr/bin/env python3
# coding=utf-8

import datetime
import time
import requests
import json
import sys
import time
from influxdb import InfluxDBClient
import traceback
import logging

logging.basicConfig(
    format = '[%(asctime)s] {%(funcName)s:%(lineno)d} %(levelname)s - %(message)s',
    # datefmt = '%d-%m-%Y:%H:%M:%S',
    level = logging.DEBUG
)
log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stdout))

data_url = 'http://nautiluslive.org/sites/default/files/nautilus-vehicle-data.json'

def get_data():
    timestamp = int(time.time()*1000)
    try:
        r = requests.get(data_url, params = {'_' :timestamp})
        log.info("fetching json: {}\n".format(data_url))
        log.info("timestamp is: {}\n".format(timestamp))
        return r.json()
    except Exception as e:
        log.critical("exception in fetching data: {}\n".format(str(e)))
        return None

def null_formatter(val):
    return val

def asInfluxDict(vessel, record, data, formatter=null_formatter):
    """vessel is: "hercules", "argus", or "nautilus"
    record is: "depth", "temp", "tempProbe", "windSpeed" etc.
    data is a json dict from nautilus api
    formatter is a function that is called on the data value before sending to influx
    """

    influxjson = {
        "measurement": "vessel-status",
        "tags": {"vessel": vessel},
        "time": data[vessel][record]["dtmRecorded"],
        "fields": {record: float(formatter(data[vessel][record]["value"]))}
    }
    return influxjson

def eventlogAsInfluxDict(data):
    try:
        dtms = data["nautilus"]["eventlog"]["dtmRecorded"]
        logs = data["nautilus"]["eventlog"]["value"]
        influxlist = []
        for i in range(0, len(dtms)):
            if type(dtms[i]) == type("2018-22-08T12:10:10Z"):
                influxlist.append({
                    "measurement": "vessel-status",
                    "tags": {"vessel": "nautilus"},
                    "time": dtms[i],
                    "fields": {"eventlog": logs[i]}
                })
    except Exception as e:
        logging.warning("Exception parsing nautilus json data: {}".format(str(e)))
        return None
    return influxlist
def sendToInflux(data):
    # `data` is a dict from the nautiluslive API
    datapoints = [
        asInfluxDict("hercules", "depth", data, formatter = lambda val: float(-val)),
        asInfluxDict("argus",    "depth", data, formatter = lambda val: float(-val)),
        asInfluxDict("hercules", "temp", data),
        asInfluxDict("hercules", "tempProbe", data),
        asInfluxDict("nautilus", "windSpeed", data),
        asInfluxDict("nautilus", "windHeading", data),
        asInfluxDict("nautilus", "heading", data),
    ]

    datapoints = [elem for elem in datapoints if elem != None]

    client = InfluxDBClient('localhost', 8086, 'nautilus-data', 'password', 'nautilus-autofetch')
    client.create_database('nautilus-autofetch')
    client.write_points(datapoints)
    client.write_points(eventlogAsInfluxDict(data))

def main():
    prev_data = None
    while True:
        data = get_data()
        # deduplicate previously received data
        if data == prev_data:
            log.info('No new data in fetch\n')
            # store one json object per line
        else:
            try:
                with open(data_file, 'a') as fout:
                    fout.write(json.dumps(data) + '\n')
                    fout.flush()
                sendToInflux(data)
            except Exception as e:
                log.critical("Failure to save data: {}\n".format(str(e)))
                traceback.print_exc()


        prev_data = data
        time.sleep(50)

if len(sys.argv) == 2:
    data_file = sys.argv[1]
else:
    data_file = 'data/' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H-%M-%S') + '.json'
log.info('writing JSON data to %s' % data_file)

try:
    main()
except KeyboardInterrupt as e:
    exit(0)
