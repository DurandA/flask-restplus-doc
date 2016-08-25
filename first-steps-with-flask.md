# Installing Python 3
## Windows
TODO
## OSX
### Install [Homebrew](http://brew.sh/)
Open a terminal and type
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
### Install python and pip (python package manager)
```
brew install python3
```
Check version with `python3 --version`. It should output `Python 3.5` or greater. Note that *Homebrew*'s *python* package already comes with pip package manager.

## Ubuntu 14.04/16.04
### Install pip (python package manager)
```
sudo apt-get install python3-pip
pip3 install --upgrade pip
```

# Install dependencies (flask, flask-restplus, ...)
```
pip3 install Flask
pip3 install flask-restplus
```
Alternatively, you can install dependencies for a specific project according to *requirements.txt* with `pip3 install -r /path/to/requirements.txt`.

Note that *pip* install packages globally by default. If you have several Python projects with different package versions, you might want to use a tool like [virtualenv](https://virtualenv.pypa.io/en/stable/) to create isolated Python environments.

# Your first web application
## Flask
Create a `hello.py` file containing the following code (from [Flask documentation](http://flask.pocoo.org/)) and run it with `python3 hello.py`.
```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
```
Open a browser and navigate to http://localhost:5000/. Alternatively, open a terminal and make a request using [curl](https://curl.haxx.se/docs/manpage.html) with `curl http://localhost:5000`. It should display *Hello World!*.

## Flask-RESTPlus
Create a `api.py` file containing the following code (from [Flask-RESTPlus documentation](https://flask-restplus.readthedocs.io/en/stable/quickstart.html#a-minimal-api) and run it with `python3 api.py`.

Test out your API using curl
```
$ curl http://127.0.0.1:5000/hello
{"hello": "world"}
```

# Resources
TODO
