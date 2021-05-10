SHEL := /bin/bash

build:
	 docker build -t lhs --build-arg NB_USER=$$(whoami) --build-arg NB_UID=$$(id -u) .

clean:
	docker rmi lhs
