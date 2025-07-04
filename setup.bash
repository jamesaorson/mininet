#! /bin/bash

brew install bgpstream

python3 -m venv venv
source ./venv/bin/activate
CFLAGS="-I$(brew --prefix bgpstream)/include -L$(brew --prefix bgpstream)/lib" pip install pybgpstream
