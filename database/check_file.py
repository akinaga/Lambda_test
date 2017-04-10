#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
import glob

connection = psycopg2.connect("dbname=traffic")
cur = connection.cursor()
connection.autocommit = True

files = glob.glob('/home/ec2-user/Lambda_test/database/result/22f0d0a7-2ef2-4bb1-b0bb-6fa9fbbfcae7/*.txt')

for filename in files:
    f = open(filename,"r")
    d = f.read().split(",")
    dat = {}
    for t in d:
        u = t.split(":")
        dat[u[0].replace(" ", "")] = u[1]
    print dat
    cur.execute("insert into lambda_test values ('%s',%s,%s,%s,%s);" % (
            dat.get('uuid',''), dat.get('seq', 0), dat.get('inittime',0), dat.get('opentime',0), dat.get('difftime',0)))

connection.close()
sys.stderr.write('\n')
sys.stderr.flush()

