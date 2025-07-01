#! /bin/bash

brew install bgpstream 
brew install uv

uv venv
source .venv/bin/activate
uv pip install termcolor
CFLAGS='-I/opt/homebrew/include -L/opt/homebrew/lib' uv pip install pybgpstream

