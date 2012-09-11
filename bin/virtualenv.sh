#!/usr/bin/env bash

[ "${DEV_TOOLS_HOME}xxx" == "xxx" && DEV_TOOLS_HOME=${HOME}/.snakegit

VIRTUALENV_SRC=$DEV_TOOLS_HOME/var/submodules/virtualenv
[ "${VIRTUALENV_DIR}xxx" == "xxx" && VIRTUALENV_DIR=`pwd`/vendor/python

if [ ! -f $VIRTUALENV_DIR/bin/python ]
then
	/usr/bin/env python $VIRTUALENV_SRC/virtualenv.py --no-site-packages --distribute $VIRTUALENV_DIR
	rm -f distribute*.tar.gz
fi
