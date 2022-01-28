# grupa_7_suml

How to run
==========

Run with Docker
---------------

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
