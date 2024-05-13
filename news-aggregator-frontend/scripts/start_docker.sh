docker build . -t news-aggregator-frontend
docker run -it -p 5173:5173 -v ${PWD}:/usr/app --rm news-aggregator-frontend