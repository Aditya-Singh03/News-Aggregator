#!/bin/bash

curl -X 'POST' \
'http://127.0.0.1:8000/user/register' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "email_address": "john.doe@gmail.com",
          "password": "passwordThis123",
          "username": "john_doe",
          "avatar": 0
}' | jq .

export TOKEN=$(curl -X 'POST' \
    'http://127.0.0.1:8000/user/login' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
          "email_address": "john.doe@gmail.com",
          "password": "passwordThis123"
}' | jq -r .token)

export USER_ID=$(curl -X 'GET' -H "Authorization: Bearer $TOKEN" \
'http://localhost:8000/user/view' | jq -r .user.id)

curl -X 'POST' -H "Authorization: Bearer $TOKEN" \
'http://127.0.0.1:8000/user/add-preferences' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "preferences": ["topic1", "topic2"]
}' | jq .

curl -X 'GET' -H "Authorization: Bearer $TOKEN" \
'http://localhost:8000/user/get-preferences' | jq .

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

curl -X 'GET' \
"http://localhost:8000/aggregator/get-aggregation?post_id=$POST_ID" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' | jq .

curl -X 'POST' \
'http://localhost:8000/annotator/add-annotation' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "post_id": "'$POST_ID'",
          "list_topics": ["topic1", "topic2"]
}'

curl -X 'GET' \
"http://localhost:8000/annotator/get-annotation?post_id=$POST_ID" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' | jq .

curl -X 'GET' -H "Authorization: Bearer $TOKEN" \
'http://localhost:8000/recommender/get-recommendations' | jq .

export COMMENT_ID=$(curl -X 'POST' -H "Authorization: Bearer $TOKEN" \
    "http://localhost:8000/aggregator/comment" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
          "post_id": "'$POST_ID'",
          "content": "This is a comment"
}' | jq -r .comment_id)

curl -X 'GET' \
"http://localhost:8000/aggregator/get-comments?post_id=$POST_ID" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' | jq .

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/upvote-post?post_id=$POST_ID" | jq .

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/upvote-post?post_id=$POST_ID" | jq .

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/remove-upvote-post?post_id=$POST_ID" | jq .

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/downvote-post?post_id=$POST_ID" | jq .

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/remove-downvote-post?post_id=$POST_ID" | jq .

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/remove-downvote-post?post_id=$POST_ID" | jq .

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/upvote-comment?comment_id=$COMMENT_ID" | jq .

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/upvote-comment?comment_id=$COMMENT_ID" | jq .

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/remove-upvote-comment?comment_id=$COMMENT_ID" | jq .

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/remove-downvote-comment?comment_id=$COMMENT_ID" | jq .

curl -X 'PUT' -H "Authorization: Bearer $TOKEN" \
"http://localhost:8000/aggregator/downvote-comment?comment_id=$COMMENT_ID" | jq .

curl -X 'GET' \
"http://localhost:8000/user/get-user?user_id=$USER_ID" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' | jq .

curl -X 'POST' \
"http://localhost:8020/subscriber/update" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "post_id": "'$POST_ID'",
          "message": "become"
}' | jq .
