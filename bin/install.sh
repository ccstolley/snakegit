#!/usr/bin/env sh 

# Welcome message
cat <<EOM
 ____              _         ____ _ _
/ ___| _ __   __ _| | _____ / ___(_) |_
\___ \| '_ \ / _' | |/ / _ \ |  _| | __|
 ___) | | | | (_| |   <  __/ |_| | | |_ 
|____/|_| |_|\__,_|_|\_\___|\____|_|\__|

EOM
echo "This installer configures your development environment"
echo "to work with the SnakeGit set of tools.  SnakeGit "
echo "integrates standard development and build workflows "
echo "with git for a (hopefully) more consistent development"
echo "experience." 
echo ""
echo "Would you like to continue with installing [y] ?"

read INSTALL

if [ "$INSTALL" = "n" ] || [ "$INSTALL" = "N" ]; then
 echo "Sorry to hear it"
 exit
fi

# getopt on OS X is inherently broken.  We might end up with unexpected 
# behavior if it is used.  This will give people the chance to install
# homebrew and then install a good getopt.  This also affects gitflow

unamestr=`uname`

configure_os_x()
{
 which brew > /dev/null
 if [[ $? == 0 ]]
 then
	echo "Some bash features do not work nicely with OS X"
	echo "To fix this, we can install Homebrew (http://mxcl.github.com/homebrew)"
	echo "Homebrew is a package manager similar to apt-get or yum"
	echo "It can make lots of tasks a lot easier, in addition to"
	echo "fixing the issues here."
	echo ""
	echo "Would you like to install brew now (recommended) [y] ?"
	read INSTALL_BREW
	if [ "$INSTALL_BREW" == "Y" ] || [ "$INSTALL_BREW" == "y" ] || [ "$INSTALL_BREW" == "" ]
	then
	 ruby < curl -fsSkL raw.github.com/mxcl/homebrew/go
	fi
 fi
 which brew > /dev/null
 if [ $? -ne 0 ]
 then
	brew install gnu-getopt
	grep FLAGS_GET_OPT_CMD ~/.bash_profile > /dev/null
  if [ $? -ne 0 ]
	then
	 echo 'export FLAGS_GETOPT_CMD="$(brew --prefix gnu-getopt)/bin/getopt"' >> ~/.bash_profile
	 echo "To make sure that you pick up the changes made here"
	 echo "Please reload your ~/.bash_profile file:"
	 echo ". ~/.bash_profile"
	fi
 fi
}

if [ "$unamestr" = 'Darwin' ]
then
 configure_os_x
fi

#Now that that is taken care of, install snakegit
[ "${SNAKEGIT_HOME}xxx" = "xxx" ] &&  SNAKEGIT_HOME=${HOME}/.snakegit
echo "Where do you want to install SnakeGit [$SNAKEGIT_HOME] ?"
read LOCATION
if [ "$LOCATION" != "" ]
then
 SNAKEGIT_HOME=$LOCATION
fi
RCFILE=${HOME}/.bashrc
if [ "$unamestr" = "Darwin" ]
then
 RCFILE=${HOME}/.bash_profile
fi

echo "Configuring SnakeGit home in $RCFILE"
echo ""
grep SNAKEGIT_HOME $RCFILE > /dev/null
if [ $? -ne 0 ]
then
 echo "export SNAKEGIT_HOME=$SNAKEGIT_HOME" >> $RCFILE
fi

if [ ! -e $SNAKEGIT_HOME ]
then
 echo "Installing SnakeGit"
 echo ""
 git clone https://github.com/NarrativeScience/snakegit.git $SNAKEGIT_HOME >> /tmp/snakegit_install.log 2>&1
 cd $SNAKEGIT_HOME
 git submodule init >> $SNAKEGIT_HOME/install.log 2>&1
 git submodule update >> $SNAKEGIT_HOME/install.log 2>&1
fi

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

BUILD="! /usr/bin/env bash $SNAKEGIT_HOME/bin/build.sh"
OLD_BUILD=`git config --get alias.build > /dev/null`
if [ "$OLD_BUILD" != "$BUILD" ]
then
 git config --global --replace-all alias.build "$BUILD"
fi

UPLOAD="! /usr/bin/env bash $SNAKEGIT_HOME/bin/upload.sh"
OLD_UPLOAD=`git config --get alias.upload-package > /dev/null`
if [ "$OLD_UPLOAD" != "$UPLOAD" ]
then
 git config --global --replace-all alias.upload-package "$UPLOAD"
fi

TEST="! /usr/bin/env bash $SNAKEGIT_HOME/bin/test.sh"
OLD_TEST=`git config --get alias.test > /dev/null`
if [ "$OLD_TEST" != "$TEST" ]
then
 git config --global --replace-all alias.test "$TEST"
fi

LINT="! /usr/bin/env bash $SNAKEGIT_HOME/bin/lint.sh"
OLD_LINT=`git config --get alias.lint > /dev/null`
if [ "$OLD_LINT" != "$LINT" ]
then
 git config --global --replace-all alias.lint "$LINT"
fi

SLITHER="! /usr/bin/env bash $SNAKEGIT_HOME/bin/sdist.sh"
OLD_SLITHER=`git config --get alias.sdist`
if [ "$OLD_SLITHER" != "$SLITHER" ]
then
 git config --global --replace-all alias.sdist "$SLITHER"
fi

SNAKE_SHED="! /usr/bin/env bash $SNAKEGIT_HOME/bin/clean.sh"
OLD_SNAKE_SHED=`git config --get alias.dev-clean`
if [ "$SNAKE_SHED" != "$OLD_SNAKE_SHED" ]
then
 git config --global --replace-all alias.dev-clean "$SNAKE_SHED"
fi

SNAKE_UPDATE="! /usr/bin/env bash $SNAKEGIT_HOME/bin/selfupdate.sh"
OLD_SNAKE_UPDATE=`git config --get alias.selfupdate`
if [ "$SNAKE_UPDATE" != "$OLD_SNAKE_UPDATE" ]
then
 git config --global --replace-all alias.snakeupdate "$SNAKE_UPDATE"
fi

bash $SNAKEGIT_HOME/bin/selfupdate.sh
