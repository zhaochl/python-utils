#!/usr/bin/env python
# coding=utf-8
from flask import *
import logging
import json
from tree_builder import *

app = Flask(__name__)

@app.route('/get_suggestion/<inputs>')
def return_suggestion(inputs):
    logging.info('Request /get_suggestion/'+inputs)

    sugs = get_suggestion(inputs)

    result = []
    for sug in sugs:
        s = {"value":sug}
        result.append(s)

    resp = make_response(json.dumps(result))
    resp.headers['Access-Control-Allow-Origin'] = "*"

    logging.info('Return /get_suggestion/'+inputs)
    
    return resp

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S')

    logging.info('Load index tree from disk, build it if not exist.')
    load_tree()
    logging.info('Load finish.')
    app.run(host='localhost')
