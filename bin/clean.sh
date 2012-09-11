#!/usr/bin/env bash

test -f DEV_TOOLS_HOME  || DEV_TOOLS_HOME=${HOME}/.snakegit
test -z $VIRTUALENV_DIR || VIRTUALENV_DIR=vendor/python

rm -rf $VIRTUALENV_DIR
rm -rf build dist
rm -rf *.egg-info
rm -rf src/*.egg-info
