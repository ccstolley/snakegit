#!/usr/bin/env bash
[ "${DEV_TOOLS_HOME}xxx" == "xxx"     ] &&  DEV_TOOLS_HOME=${HOME}/.snakegit
[ "${VIRTUALENV_DIR}xxx" == "xxx"     ] &&  VIRTUALENV_DIR=vendor/python
[ "${PIP_DOWNLOAD_CACHE}xxx" == "xxx" ] &&  PIP_DOWNLOAD_CACHE=vendor/cache


/usr/bin/env bash $DEV_TOOLS_HOME/bin/virtualenv.sh

echo "Installing libraries"
PIP_DOWNLOAD_CACHE=$PIP_DOWNLOAD_CACHE $VIRTUALENV_DIR/bin/pip install \
	--no-deps --extra-index-url `git config --get pypi.scheme`://`git config --get pypi.user`@`git config --get pypi.host`/simple/ \
	-r requirements.txt > /dev/null

