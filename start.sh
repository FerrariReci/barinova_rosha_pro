#!/bin/bash

# Exit early on errors
curl https://pyenv.run | bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
pyenv install 3.8
set -eu

# Python buffers stdout. Without this, you won't see what you "print" in the Activity Logs
export PYTHONUNBUFFERED=true

# Install Python 3 virtual env
VIRTUALENV=./venv

if [ ! -d $VIRTUALENV ]; then
	  python3 -m venv $VIRTUALENV
fi

# Install pip into virtual environment
if [ ! -f $VIRTUALENV/bin/pip ]; then
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | $VIRTUALENV/bin/python
fi

$VIRTUALENV/bin/python3 -m pip install -U pip
# Install the requirements
$VIRTUALENV/bin/pip install -r requirements.txt

# Run your glorious application
$VIRTUALENV/bin/python3 server.py
