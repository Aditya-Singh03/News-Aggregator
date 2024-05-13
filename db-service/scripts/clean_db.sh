#!/bin/bash

curl -X 'GET' \
'http://127.0.0.1:8000/clean_db' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' | jq .
