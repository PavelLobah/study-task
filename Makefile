# docker
docker-build:
	docker build -t myproject .
docker-run:
	docker run -p 8000:8000 --name mycontainer myproject

# docker-compose
docker-compose-build:
	docker-compose up -d --build

