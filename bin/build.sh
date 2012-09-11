#!/usr/bin/env bash
test -z $DEV_TOOLS_HOME || DEV_TOOLS_HOME=${HOME}/.snakegit
test -z $VIRTUALENV_DIR || VIRTUALENV_DIR=vendor/python
test -z $PIP_DOWNLOAD_CACHE || PIP_DOWNLOAD_CACHE=vendor/cache

/usr/bin/env bash $DEV_TOOLS_HOME/bin/virtualenv.sh

echo "Installing libraries"
PIP_DOWNLOAD_CACHE=$PIP_DOWNLOAD_CACHE $VIRTUALENV_DIR/bin/pip install \
	--no-deps --extra-index-url `git config --get pypi.scheme`://`git config --get pypi.user`@`git config --get pypi.host`/simple/ \
	-r requirements.txt > /dev/null

