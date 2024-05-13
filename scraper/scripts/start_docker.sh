#!/bin/bash

docker build . -t annotator

docker run -it -v ${PWD}:/code -p 8020:8020 --rm annotator
