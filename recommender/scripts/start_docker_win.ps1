
docker build . -t recommender

docker run -p 8030:8030 -it -v ${PWD}:/code --rm recommender 
