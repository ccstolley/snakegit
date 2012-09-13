#!/usr/bin/env sh

[ "${DEV_TOOLS_HOME}xxx" = "xxx" ]  && DEV_TOOLS_HOME=${HOME}/.snakegit
[ "${VIRTUALENV_DIR}xxx" = "xxx" ]  && VIRTUALENV_DIR=vendor/python

/usr/bin/env bash $DEV_TOOLS_HOME/bin/build.sh

$VIRTUALENV_DIR/bin/python setup.py sdist
