#!/bin/bash
sudo kill -9 `ps -elf|grep datastash|awk '{print $4}'`
echo 'success'
