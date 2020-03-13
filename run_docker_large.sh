#!/bin/bash

docker run -m 100g --cpus=31 -v $HOME/avvir/data:/source/OpenSfM/data/avvir -it opensfm
