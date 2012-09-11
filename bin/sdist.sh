#!/usr/bin/env bash

test -z $DEV_TOOLS_HOME || DEV_TOOLS_HOME=${HOME}/.snakegit
test -z $VIRTUALENV_DIR || VIRTUALENV_DIR=vendor/python

/usr/bin/env bash $DEV_TOOLS_HOME/bin/build.sh

$VIRTUALENV_DIR/bin/python setup.py sdist
