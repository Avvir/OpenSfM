#!/bin/bash

docker run -m 8g --cpus=4 -v $HOME/avvir/data:/source/OpenSfM/data/avvir -it opensfm
