#!/usr/bin/env python
# coding=utf-8
import json
import logging
import time
import urllib
def get_json_from_url(url):
    search_res = None    
    while True:
        try:
            search_res = json.loads(urllib.urlopen(url).read())
            break
        except Exception, e:
            logging.error('Search error: %s, %s'%(str(e), url))
            time.sleep(5)
    return search_res
