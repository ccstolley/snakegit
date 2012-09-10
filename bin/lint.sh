#!/usr/bin/env bash
test -v SNAKEGIT_HOME || SNAKEGIT_HOME=${HOME}/.snakegit

test -v VIRTUALENV_DIR || VIRTUALENV_DIR=./vendor/python

$VIRTUALENV_DIR/bin/pip install $SNAKEGIT_HOME/var/submodules/pylint
$VIRTUALENV_DIR/bin/pip install $SNAKEGIT_HOME/var/submodules/pep8
$VIRTUALENV_DIR/bin/pip install $SNAKEGIT_HOME/var/submodules/pyflakes

function usage {
  echo "Usage: lint.sh"
  echo "-l|--pylint               Run PyLint"
  echo "-p|--pep8                 Run Pep8"
  echo "-f|--pyflakes             Run PyFlakes"
  echo "-s|--src value            Lint the specified src directory"
  echo "-o|--output dirctory      Write to the specified output directory"
  echo "-m|--module value         Module to lint"
  exit 1
}

if ! ARGS=$(getopt -o lpfs:o:m: -l pylint,pep8,pyflakes,src:,output:,module: -- "$@")
then
  usage
fi

eval set -- $ARGS

while [ $# -gt 0 ]
do
  case "$1" in
    -l|--pylint)
      PYLINT=true
      ;;
      
    -p|--pep8)
      PEP8=true
      ;;
      
    -f|--pyflakes)
      PYFLAKES=true
      ;;

    -s|--src)
      SRC_DIR=$2
      shift;;

    -o|--output)
      TEST_OUTPUT_DIR="$2"
      shift;;
    
    -m|--module)
      MODULE="$2"
      shift;;

    --)
      shift;
      break;;
    (*)
      break;;
  esac
  shift
done

function require_src {
  if [ ! -v SRC_DIR ]
  then
    echo "You must supply a source package with -s"
    exit 1
  fi
}

function require_module {
  if [ ! -v MODULE ]
  then
    echo "You must supply a module to lint with -m"
    exit 1
  fi
}

$VIRTUALENV_DIR/bin/python setup.py install

test -v TEST_OUTPUT_DIR || TEST_OUTPUT_DIR=test_results

mkdir -p $TEST_OUTPUT_DIR


if [ -v PYLINT ]
then
  require_module
  test -v MODULE ||$VIRTUALENV_DIR/bin/pylint -f parseable $MODULE | tee $TEST_OUTPUT_DIR/pylint.txt 
fi

if [ -v PEP8 ] 
then
  require_src
  $VIRTUALENV_DIR/bin/pep8 --format=pylint $SRC_DIR | tee $TEST_OUTPUT_DIR/pep8.txt
fi

if [ -v PYFLAKES ]
then
  require_src
  $VIRTUALENV_DIR/bin/pyflakes $SRC_DIR | awk -F\: '{printf "%s:%s: [E]%s\n", $1, $2, $3}' | tee $TEST_OUTPUT_DIR/pyflakes.txt 
fi
