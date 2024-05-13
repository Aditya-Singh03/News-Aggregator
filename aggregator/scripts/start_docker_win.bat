
docker build . -t aggregator

docker run -p 8010:8010 -it -v ./code --rm aggregator 
