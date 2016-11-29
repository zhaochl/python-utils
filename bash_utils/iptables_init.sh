#!/bin/bash
#http://www.pc811.com/6/7/26003.html
iptables -F
service iptables save
service iptables restart

