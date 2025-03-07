# kiali demo

## Start apps
Greet App:
```
docker run -it --rm  --net=host  localhost/kialidemo:latest greet-app  --czech-svc='http://localhost:8083/' --spanish-svc='http://localhost:8082/' --english-svc='http://localhost:8081/'
```

English App:
```
docker run -it --rm  --net=host localhost/kialidemo:latest english-app  --spanish-svc='http://localhost:8082/chained' --flask-port=8081
```

Spanish App:
```
docker run -it --rm  --net=host localhost/kialidemo:latest spanish-app  --czech-svc='http://localhost:8083/' --flask-port=8082
```

Czech App:
```
docker run -it --rm  --net=host localhost/kialidemo:latest czech-app --flask-port=8083
```

## Usage

```
$ curl localhost:8080/
Greet app: Hello World! | Hello Mundo! | Ahoj světe!
```

```
$ curl localhost:8080/chained
Chained: Hello World! -> Hello Mundo! -> Ahoj světe!
```

## Build container image

```
$ docker build . -t docker.io/devopstestaccount/kialidemo:1.0
$ docker push docker.io/devopstestaccount/kialidemo:1.0

$ docker build . -t quay.io/mmqaz/kialidemo:0.0
$ docker push quay.io/mmqaz/kialidemo:0.0
```
