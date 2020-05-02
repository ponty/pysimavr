FROM ubuntu:latest
MAINTAINER x

RUN apt-get update && \
    apt-get -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install \
    arduino avrdude \
    gcc libelf-dev \
    freeglut3-dev scons swig \
    python-pip python-dev

RUN pip install pysimavr

CMD /bin/bash

