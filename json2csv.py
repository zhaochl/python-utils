#!/usr/bin/env python
# coding=utf-8

import json
import csv

f = open('p.json', encoding='utf-8')
data = json.load(f)
f.close()
import pprint
print(len(data))
writer = csv.writer(open('dict.csv', 'w', encoding='utf-8'))
writer.writerow([data[0]['_source'].keys()])
for line in data:
        writer.writerow([line['_source'].values()])