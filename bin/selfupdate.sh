#!/usr/bin/env bash

[ "xxx${SNAKEGIT_HOME}" == "xxx" ] && SNAKEGIT_HOME=${HOME}/.snakegit

cd $SNAKEGIT_HOME

git pull origin master
