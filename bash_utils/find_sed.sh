#!/bin/bash
find -name "*.py"|xargs sed -i "s/user_name/root/g"
find -name "*.py"|xargs sed -i "s/'ir'/\"ir01\.io\"/g"
