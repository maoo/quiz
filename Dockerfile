FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y librsvg2-bin && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /work 