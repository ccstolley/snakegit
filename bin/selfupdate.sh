#!/usr/bin/env bash

echo "Checking for updates"
[ "xxx${SNAKEGIT_HOME}" == "xxx" ] && SNAKEGIT_HOME=${HOME}/.snakegit

cd $SNAKEGIT_HOME

git pull origin master
git submodule updates

git config --get-regexp github.* > /dev/null

function register_github {
echo "Registering with github"
}

function unregister_github {
echo "Unregister with github"
}

if [ $? -eq 0 ]
then
  echo "You already have github configured in your ~/.gitconfig"
  echo ""
  echo "Do you want to reregister your account [n]?"
  read REGISTER
  if [ "$REGISTER" == "y" ] || [ "$REGISTER" == "Y" ]
  then
    unregister_github
    register_github
  fi
else
  register_github
fi

