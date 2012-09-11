#!/usr/bin/env bash

[ "${DEV_TOOLS_HOME}xxx" == "xxx" ] && DEV_TOOLS_HOME=${HOME}/.snakegit
[ "${VIRTUALENV_DIR}xxx" == "xxx" ] && VIRTUALENV_DIR=vendor/python

rm -rf $VIRTUALENV_DIR
rm -rf build dist
rm -rf *.egg-info
rm -rf src/*.egg-info
