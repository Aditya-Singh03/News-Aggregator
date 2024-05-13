#!/bin/bash

curl -X 'POST' \
'http://localhost:8010/observer/subscribe' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "ip_address": "annotator",
          "port": 8020
}' | jq .