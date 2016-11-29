#!/usr/bin/env python
# coding=utf-8

import traceback
try:
    raise SyntaxError, "traceback test"
except:
    traceback.print_exc()
