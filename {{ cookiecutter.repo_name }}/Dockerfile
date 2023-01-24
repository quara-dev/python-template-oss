ARG BASE_IMAGE=python:3.10-slim

FROM $BASE_IMAGE

ENV PROJECT_NAME="{{ cookiecutter.project_name }}"

# Build must be performed before building Docker image
# wheelhouse directory is expected to exist with path ./dist/wheelhouse
# Run the following commands BEFORE building docker image:
#  python3 scripts/install.py
#  inv wheelhouse
RUN --mount=target=/wheelhouse,type=bind,source=dist/wheelhouse \
    python3 -m pip install -U pip setuptools wheel --no-cache-dir \
    && python3 -m pip install $PROJECT_NAME --no-cache-dir --no-index --find-links /wheelhouse
