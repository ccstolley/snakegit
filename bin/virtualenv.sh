#!/usr/bin/env bash

[ "${SNAKEGIT_HOME}xxx" == "xxx" ] && SNAKEGIT_HOME=${HOME}/.snakegit

VIRTUALENV_SRC=$SNAKEGIT_HOME/var/submodules/virtualenv
[ "${VIRTUALENV_DIR}xxx" == "xxx" ] && VIRTUALENV_DIR=`pwd`/vendor/python

if [ ! -f $VIRTUALENV_DIR/bin/python ]
then
	/usr/bin/env python $SNAKEGIT_HOME/bin/virtualenv --distribute $VIRTUALENV_DIR
	rm -f distribute*.tar.gz
fi
