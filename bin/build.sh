#!/usr/bin/env sh
[ "${DEV_TOOLS_HOME}xxx" = "xxx"     ] &&  DEV_TOOLS_HOME=${HOME}/.snakegit
[ "${VIRTUALENV_DIR}xxx" = "xxx"     ] &&  VIRTUALENV_DIR=vendor/python
[ "${PIP_DOWNLOAD_CACHE}xxx" = "xxx" ] &&  PIP_DOWNLOAD_CACHE=vendor/cache


/usr/bin/env bash $DEV_TOOLS_HOME/bin/virtualenv.sh

echo "Installing libraries"

# Acquire a temporary token so that you don't have to enter your password
# over and over again
tmp_token=`curl -s -k -u $(git config --get pypi.user) $(git config --get pypi.scheme)://$(git config --get pypi.host)/token`
uid_key=`python -c "import json ; result = json.loads('$tmp_token') ; print '{0};{1}'.format(result['uid'], result['key'])"`
uid=$(echo $uid_key | cut -d';' -f1)
key=$(echo $uid_key | cut -d';' -f2)
PIP_DOWNLOAD_CACHE=$PIP_DOWNLOAD_CACHE $VIRTUALENV_DIR/bin/pip install \
	--no-deps --extra-index-url `git config --get pypi.scheme`://$uid:$key@`git config --get pypi.host`/simple/ \
	-r requirements.txt

