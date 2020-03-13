#!/bin/bash

if [ $# -ne 1 ]; then
        echo 'No docker image specified'
            exit 1
        fi


docker run -m 100g --cpus=31 -v $HOME/avvir/data:/source/OpenSfM/data/avvir -it $1
