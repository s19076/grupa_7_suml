# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
# runtime dependencies for opencv
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx libglib2.0-0
# torch needs to be installed first due to dependency issues
# (basicsr tries to import torch in setup.py before torch is installed)
RUN sed -n '/^-/p; /^torch/p' requirements.txt | pip install -r /dev/stdin
RUN pip install -r requirements.txt

COPY model.py model.py
# RUN python model.py download-models

COPY . .

CMD FLASK_DEBUG=1 FLASK_APP=main flask run -h 0.0.0.0
