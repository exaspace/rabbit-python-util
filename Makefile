# This file is only needed to build a docker image for this project
# If you have python3 & pip installed, you can instead just run the code directly.
# To build the image into your local docker cache run `make latest`.

REGISTRY=  exaspace
IMAGE    = rabbit-python-util
VERSION  = $(shell git describe --tags)

DOCKER=$(shell docker info >/dev/null 2>&1 && echo "docker" || echo "sudo docker")

all: latest

build:
	$(DOCKER) build $(build_opts) -t $(REGISTRY)/$(IMAGE):$(VERSION) ./

latest: build
	$(DOCKER) tag $(REGISTRY)/$(IMAGE):$(VERSION) $(REGISTRY)/$(IMAGE):latest
