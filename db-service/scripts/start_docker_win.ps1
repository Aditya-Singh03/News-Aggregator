
docker build . -t db-service

docker run -p 8000:8000 -it -v ${PWD}:/code --rm db-service 
