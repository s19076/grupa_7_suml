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
```
docker build . --tag suml
```

Start a new container:
```
docker run --name suml-container -i -t -p 5000:5000 suml
```

Run directly
------------

Install required packages:
```
pip install -r requirements.txt
```

Run the app:
```
python main.py
```
