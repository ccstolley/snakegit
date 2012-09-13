#!/usr/bin/env sh

[ "${SNAKEGIT_HOME}xxx" = "xxx"  ] &&  SNAKEGIT=${HOME}/.snakegit
[ "${VIRTUALENV_DIR}xxx" = "xxx" ] &&  VIRTUALENV_DIR=vendor/python

DOC_SRC_DIR=${PWD}/docs/source
DOC_BUILD_DIR=${PWD}/docs/build


if [ -d "${DOC_SRC_DIR}" ]
then
	echo "Running sphinx-apidoc..."
  PACKAGES=`${VIRTUALENV_DIR}/bin/python setup.py --provides`
	for p in $PACKAGES
	do
		export PYTHONPATH=${PWD}/src:${PWD}:${VIRTUALENV_DIR}/lib/python2.7/site-packages:${VIRTUALENV_DIR}/lib/python2.6/site-packages
		${SNAKEGIT_HOME}/bin/sphinx-apidoc -f -o ${DOC_SRC_DIR} src/$p
	done
	${SNAKEGIT_HOME}/bin/sphinx-build ${DOC_SRC_DIR} ${DOC_BUILD_DIR}
else
	echo "No local docs directory in ${PWD}..."
fi
