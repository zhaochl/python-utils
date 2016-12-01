#!/bin/bash
for file in $(ls _bash_/)
do
    echo start call $file
    bash _bash_/$file
    echo call $file ok
done

