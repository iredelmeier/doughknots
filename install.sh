#!/bin/bash

# install and load python 3.7
curl https://pyenv.run | bash

export PATH="/app/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv install 3.7.4

pyenv local 3.7.4 # ???

# install dependencies
pip install pipenv

pipenv install --dev
