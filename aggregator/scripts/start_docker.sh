#!/bin/bash

docker build . -t aggregator

docker run -it -v ${PWD}:/code -p 8010:8010 --rm aggregator
