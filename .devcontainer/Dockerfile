ARG VERSION=3.10
ARG VARIANT=bullseye

FROM mcr.microsoft.com/devcontainers/python:${VERSION}-${VARIANT}

# Install azd
RUN export DEBIAN_FRONTEND=noninteractive \
     && apt-get update && apt-get install -y xdg-utils \
     && apt-get clean -y && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://aka.ms/install-azd.sh | bash

RUN python3 -m pip install --upgrade pip