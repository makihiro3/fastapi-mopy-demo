# fastapi-mopy-demo

Build a OCI image(docker image) of fastapi demo app by [cmdjulian/mopy](https://github.com/cmdjulian/mopy)

## build 

See also [Makefile](Makefile)

```bash
docker buildx build -t fastapi-demo -f Mopyfile.yaml .
```

## run

```bash
docker run -p 5000:5000 fastapi-demo
```
