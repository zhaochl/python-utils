#!/bin/bash
iptables -I INPUT -i eth1 -p tcp --dport 9099 -j DROP
iptables -I OUTPUT -o eth1 -p tcp --sport 9099 -j DROP

service iptables save
service iptables restart
service iptables status

