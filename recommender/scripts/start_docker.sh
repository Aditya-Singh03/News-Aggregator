#!/bin/bash

docker build . -t recommender

docker run -it -v ${PWD}:/code -p 8030:8030 --rm recommender
