.PHONY: build run

build:
	docker buildx build -t fastapi-demo -f Mopyfile.yaml .
run:
	docker run -p 5000:5000 fastapi-demo
