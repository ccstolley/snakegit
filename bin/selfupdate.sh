#!/usr/bin/env bash

test -z $SNAKEGIT_HOME || SNAKEGIT_HOME=${HOME}/.snakegit

cd $SNAKEGIT_HOME

git pull origin master
