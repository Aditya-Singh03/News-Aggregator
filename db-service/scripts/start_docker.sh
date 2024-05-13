#!/bin/bash

docker build . -t db-service

docker run -it -v ${PWD}:/code -p 8000:8000 --rm db-service
