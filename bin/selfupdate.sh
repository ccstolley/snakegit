#!/usr/bin/env sh

echo "Checking for updates"
[ "xxx${SNAKEGIT_HOME}" = "xxx" ] && SNAKEGIT_HOME=${HOME}/.snakegit

cd $SNAKEGIT_HOME

git pull origin master >> $SNAKEGIT_HOME/install.log
git submodule init >> $SNAKEGIT_HOME/install.log
git submodule update >> $SNAKEGIT_HOME/install.log

# Configure PyPi username
current_username=`git config --global --get pypi.user`
echo "Please enter your PyPi username: [$current_username]"
read USERNAME

if [ "xxx${USERNAME}" != "xxx" ] && [ "$USERNAME" != "$current_username" ]
then	
 git config --global --replace-all pypi.user $USERNAME
 git config --global --replace-all pypi.host repo.n-s.us
 git config --global --replace-all pypi.scheme https
fi

# Install git aliases
echo "Now installing git aliases"
echo ""

aliases=$(cat ${SNAKEGIT_HOME}/aliases.txt)
for alias in $aliases 
do
 KEY=$(echo $alias | cut -d: -f1 )
 COMMAND=$(echo $alias | cut -d: -f2 )
 if [ "$OLD_COMMAND" != "$COMMAND" ]
 then
	git config --global --replace-all $KEY "!/usr/bin/env sh ${SNAKEGIT_HOME}/bin/$COMMAND"
 fi
done


echo "Configuring your github account"
echo ""


register_github() {
  FORMATTED_AUTH=`curl -u $1 -d '{"scopes": ["repo","gist"], "note": "SnakeGit tools"}' https://api.github.com/authorizations`
  echo $FORMATTED_AUTH | grep message > /dev/null
  if [ $? -eq 0 ]
  then
    ERROR_MESSAGE=`echo $FORMATTED_AUTH | tr -d '\n'`
    MESSAGE=`python -c "import json; data = json.loads('$ERROR_MESSAGE') ; print data[\"message\"]"`
    echo "Github Error: $MESSAGE"
    exit 1
  fi
  AUTH=`echo $FORMATTED_AUTH | tr -d '\n'`
  TOKEN=`python -c "import json; data = json.loads('$AUTH') ; print data[\"token\"]"`
  URL=`python -c "import json; data = json.loads('$AUTH') ; print data[\"url\"]"`
  git config --global --replace-all github.token $TOKEN
  git config --global --replace-all github.url $URL
  git config --global --replace-all github.user $1
}

unregister_github() {
  curl -X DELETE -u $1 $AUTH_URL >> $SNAKEGIT_HOME/install.log 2>&1 
}

git config --get github.token > /dev/null
if [ $? -eq 0 ]
then
  echo "You already have github configured in your ~/.gitconfig"
  echo ""
  read -p "Do you want to reregister your account [n]? " REGISTER
  if [ "$REGISTER" = "y" ] || [ "$REGISTER" = "Y" ]
  then
    USER=`git config --get github.user`
    #unregister_github $USER
    register_github $USER
  fi
else
  read -p "Github Username: " USER
  register_github $USER
fi

# Install and Configure virtualenv
if [ ! -f $SNAKEGIT_HOME/bin/python ] 
then
 echo "Install and Configure the root virtualenv."
 echo "This will be used to generate other virtualenv's"
 echo "and to hold common tools, e.g. nose."
 /usr/bin/env python $SNAKEGIT_HOME/var/submodules/virtualenv/virtualenv.py --distribute $SNAKEGIT_HOME >> /tmp/snakegit_install.log 2>&1
 $SNAKEGIT_HOME/bin/pip install $SNAKEGIT_HOME/var/submodules/virtualenv
fi

GEARBOX="! /usr/bin/env sh $SNAKEGIT_HOME/bin/gearbox.sh"
OLD_GEARBOX=`git config --get alias.gearbox`
if [ "$GEARBOX" != "$OLD_GEARBOX" ]
then
  git config --global --replace-all alias.gearbox "$GEARBOX"
 fi

SNAKEUPDATE="! /usr/bin/env sh $SNAKEGIT_HOME/bin/selfupdate.sh"
OLD_SNAKEUPDATE=`git config --get alias.snakeupdate`
if [ "$SNAKEUPDATE" != "$OLD_SNAKEUPDATE" ]
then
  git config --global --replace-all alias.snakeupdate "$SNAKEUPDATE"
 fi

PULLREQ="! /usr/bin/env python $SNAKEGIT_HOME/bin/pullreq.py"
OLD_PULLREQ=`git config --get alias.pullreq`
if [ "$PULLREQ" != "$OLD_PULLREQ" ]
then
  git config --global --replace-all alias.pullreq "$PULLREQ"
 fi
