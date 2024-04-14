.PHONY: build run

build:
	poetry export --only main >requirements.txt
	docker buildx build -t fastapi-demo -f Mopyfile.yaml .
run:
	docker run -p 5000:5000 fastapi-demo
