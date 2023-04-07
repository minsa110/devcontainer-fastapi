ARG VERSION=3.10
ARG VARIANT=bullseye

FROM mcr.microsoft.com/devcontainers/python:${VERSION}-${VARIANT}

# Install azd
RUN export DEBIAN_FRONTEND=noninteractive \
     && apt-get update && apt-get install -y xdg-utils \
     && apt-get clean -y && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://aka.ms/install-azd.sh | bash

RUN python3 -m pip install --upgrade pip

# Copy requirements.txt (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no requirements.txt exists.
COPY requirements.txt* .devcontainer/noop.txt /tmp/pip/
RUN if [ -f "/tmp/pip/requirements.txt" ]; then umask 0002 && python3 -m pip install -r /tmp/pip/requirements.txt && sudo rm -rf /tmp/pip; fi

# sudo apt update
# sudo apt-get -y install ufw
# sudo ufw allow 8000