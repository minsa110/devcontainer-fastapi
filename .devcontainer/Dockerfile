ARG VARIANT=bullseye
FROM mcr.microsoft.com/devcontainers/python:0-${VARIANT}

RUN python3 -m pip install fastapi uvicorn

# Copy requirements.txt (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no requirements.txt exists.
COPY requirements.txt* .devcontainer/noop.txt /tmp/pip-tmp/
RUN if [ -f "/tmp/pip-tmp/requirements.txt" ]; then umask 0002 && python3 -m pip install /tmp/pip-tmp/requirements.txt && sudo rm -rf /tmp/pip-tmp; fi