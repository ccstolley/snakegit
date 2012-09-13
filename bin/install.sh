#!/bin/sh
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
	 curl -fsSkL raw.github.com/mxcl/homebrew/go | ruby
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

sh $SNAKEGIT_HOME/bin/selfupdate.sh
