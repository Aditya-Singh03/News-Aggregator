#!/bin/bash

curl -X 'POST' \
'http://127.0.0.1:8000/user/register' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "email_address": "lifewhiz101@gmail.com",
          "password": "lifewhiz101",
          "username": "lifewhiz101",
          "avatar": 0
}' | jq .

export TOKEN=$(curl -X 'POST' \
    'http://127.0.0.1:8000/user/login' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
          "email_address": "lifewhiz101@gmail.com",
          "password": "lifewhiz101"
}' | jq -r .token)

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
'http://127.0.0.1:8000/user/update-user' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "email_address": "lifewhiz@gmail.com",
          "username": "lifewhiz",
          "avatar": 2,
          "password": "lifewhiz101"
}' | jq .

curl -X 'POST' -H "Authorization: Bearer $TOKEN" \
'http://127.0.0.1:8000/user/add-preferences' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "preferences": ["topic1", "topic2"]
}' | jq .

export POST_ID=$(curl -X 'POST' \
    'http://localhost:8000/aggregator/add-aggregation' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
          "title": "Sample Post",
          "link": "https://www.google.com",
          "media": "https://www.google.com",
          "author": "John Doe",
          "date": "2021-09-01"
}' | jq -r .post_id)

export POST_ID_2=$(curl -X 'POST' \
    'http://localhost:8000/aggregator/add-aggregation' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
          "title": "Sample Post 2",
          "link": "https://www.amazon.com",
          "media": "https://www.amazon.com",
          "author": "John Boe",
          "date": "2022-09-01"
}' | jq -r .post_id)


curl -X 'POST' \
'http://localhost:8000/annotator/add-annotation' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "post_id": "'$POST_ID'",
          "list_topics": ["topic1", "topic2"]
}' | jq .

curl -X 'POST' \
'http://localhost:8000/annotator/add-annotation' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "post_id": "'$POST_ID_2'",
          "list_topics": ["topic1", "topic2"]
}' | jq .

curl -X 'POST' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/comment" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "post_id": "'$POST_ID'",
          "content": "This is a comment"
}' | jq -r .comment_id


curl -X 'POST' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/comment" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "post_id": "'$POST_ID'",
          "content": "This is a comment 2"
}' | jq -r .comment_id


curl -X 'POST' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/comment" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "post_id": "'$POST_ID_2'",
          "content": "This is a comment 3"
}' | jq -r .comment_id

curl -X 'POST' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8020/llm/generate-summary" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "post_id": "3b32cf7f-d816-4ebd-b714-e9b76aecdb51",
          "text": "In general, a sample is a limited quantity of something which is intended to be similar to and represent a larger amount of that thing(s)."
}' | jq .


curl -X 'POST' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8020/llm/generate-title" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "post_id": "3b32cf7f-d816-4ebd-b714-e9b76aecdb51",
          "text": "In general, a sample is a limited quantity of something which is intended to be similar to and represent a larger amount of that thing(s)."
}' | jq .

curl -X 'POST' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8020/llm/prompt" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "prompt": "Hello, what is your name?"
}' | jq .

curl http://ollama:11434/api/generate -d '{     "model": "gemma",
  "prompt": "Generate a social media post title using only 5 words and at most 1 sentence for the following text and only return the title: Ukraine has begun using long-range ballistic missiles secretly provided by the US against invading Russian forces, American officials have confirmed ",
  "raw": true,
  "stream": false
}'

curl http://localhost:11434/api/pull -d '{
  "name": "gemma"
}'