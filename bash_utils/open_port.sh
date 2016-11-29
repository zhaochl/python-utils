#!/bin/bash
iptables -I INPUT -i eth1 -p tcp --dport 1111 -j ACCEPT
iptables -I OUTPUT -o eth1 -p tcp --sport 1111 -j ACCEPT

service iptables save
service iptables restart
service iptables status

