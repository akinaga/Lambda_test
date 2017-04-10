#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request
import datetime
import time

app = Flask(__name__)

queueName = 'Lambda_test'


@app.route('/', methods=['GET', 'POST'])
def timing():

    inittime = request.args.get('inittime', default=0, type=int)
    uuid = request.args.get('uuid', default='test', type=str)
    seq = request.args.get('seq', default=0, type=int)

    now = datetime.datetime.now()
    opentime = int(time.mktime(now.timetuple()) * 1000 + now.microsecond / 1000)

    difftime = opentime - inittime

    dat = {}
    dat['seq'] = seq
    dat['opentime'] = opentime
    dat['inittime'] = inittime
    dat['uuid'] = uuid
    dat['difftime'] = difftime

    import boto3
    import json
    session = boto3.session.Session(region_name='ap-northeast-1')
    sqs = session.resource('sqs')
    response = sqs.get_queue_by_name(QueueName=queueName).send_message(MessageBody=json.dumps(dat))

    return json.dumps(dat)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)
