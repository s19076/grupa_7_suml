# grupa_7_suml
[![python lint](https://github.com/s19076/grupa_7_suml/actions/workflows/pylint.yml/badge.svg)](https://github.com/s19076/grupa_7_suml/blob/main/.github/workflows/pylint.yml)
[![docker](https://github.com/s19076/grupa_7_suml/actions/workflows/docker-image.yml/badge.svg)](https://github.com/s19076/grupa_7_suml/blob/main/.github/workflows/docker-image.yml)

This web app can be used for improving the quality of old or
low resolution photos of faces. Face restoration is performed
by [GFPGAN](https://github.com/TencentARC/GFPGAN).

How to run
==========

Run with Docker
---------------

Install Docker: <https://docs.docker.com/get-started/>

Build the image:
```shell script
docker build . --tag suml
```

Start a new container:
```shell script
docker run --name suml-container -i -t -p 5000:5000 suml
```

Run directly
------------

Install required packages:
```shell script
pip install torch==1.10.1+cpu torchvision==0.11.2+cpu torchaudio==0.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
pip install -r requirements.txt
```

Run the app:
```shell script
python main.py
```
