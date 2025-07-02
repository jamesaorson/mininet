#! /bin/bash

brew install bgpstream 

python3 -m venv venv
source ./venv/bin/activate
CFLAGS='-I/opt/homebrew/include -L/opt/homebrew/lib' pip install pybgpstream
