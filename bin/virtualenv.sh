#!/usr/bin/env bash

test -z $DEV_TOOLS_HOME || DEV_TOOLS_HOME=${HOME}/.snakegit

VIRTUALENV_SRC=$DEV_TOOLS_HOME/var/submodules/virtualenv
test -z $VIRTUALENV_DIR || VIRTUALENV_DIR=`pwd`/vendor/python

if [ ! -f $VIRTUALENV_DIR/bin/python ]
then
	/usr/bin/env python $VIRTUALENV_SRC/virtualenv.py --no-site-packages --distribute $VIRTUALENV_DIR
	rm -f distribute*.tar.gz
fi
