
docker build . -t recommender

docker run -p 8030:8030 -it -v ./code --rm recommender 
