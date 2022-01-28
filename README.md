# grupa_7_suml

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
pip install -r requirements.txt
```

Run the app:
```shell script
python main.py
```
