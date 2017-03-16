#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import boto3
import json
import sys

connection = psycopg2.connect("dbname=traffic")
cur = connection.cursor()
connection.autocommit = True

session = boto3.session.Session(region_name='ap-northeast-1')
sqs = session.resource('sqs')

# キューの名前を指定して
name = 'Lambda_test'
queue = sqs.get_queue_by_name(QueueName=name)
while True:
    # メッセージを取得
    msg_list = queue.receive_messages(MaxNumberOfMessages=10)
    if msg_list:
        for message in msg_list:
            dat = json.loads(message.body)
            sys.stderr.write('\r\033[K' + str(dat))
            sys.stderr.flush()
            # print dat
            cur.execute("insert into lambda_test values ('%s',%s,%s,%s,%s);" % (
                dat.get('uuid',''), dat.get('seq', 0), dat.get('inittime',0), dat.get('opentime',0), dat.get('difftime',0)))
            # cur.fetchall()
            message.delete()
    else:
        # メッセージがなくなったらbreak
        break

connection.close()
sys.stderr.write('\n')
sys.stderr.flush()

