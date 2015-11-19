#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import commands
output = os.popen('ls')
print output.read()

print '----------------------------'
(status, output) = commands.getstatusoutput('ls')
print status, output
