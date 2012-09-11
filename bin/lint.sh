#!/usr/bin/env sh
[ "${SNAKEGIT_HOME}xxx" = "xxx" ]  && SNAKEGIT_HOME=${HOME}/.snakegit

[ "${VIRTUALENV_DIR}xxx" = "xxx" ] && VIRTUALENV_DIR=./vendor/python

$VIRTUALENV_DIR/bin/pip install $SNAKEGIT_HOME/var/submodules/pylint
$VIRTUALENV_DIR/bin/pip install $SNAKEGIT_HOME/var/submodules/pep8
$VIRTUALENV_DIR/bin/pip install $SNAKEGIT_HOME/var/submodules/pyflakes

usage()
{
  echo "Usage: lint.sh"
  echo "-l              Run PyLint"
  echo "-p              Run Pep8"
  echo "-f              Run PyFlakes"
  echo "-s=value        Lint the specified src directory"
  echo "-o=dirctory     Write to the specified output directory"
  echo "-m=value        Module to lint"
  exit 1
}

while getopts lpfs:o:m: o
do
  case "$o" in
    l)
      PYLINT=true
      ;;
      
    p)
      PEP8=true
      ;;
      
    f)
      PYFLAKES=true
      ;;

    s)
      SRC_DIR="$OPTARG"
      ;;

    o)
      TEST_OUTPUT_DIR="$OPTARG"
      ;;
    
    m)
      MODULE="$OPTARG"
      ;;

    [?])
     usage 
     exit 1
     ;;
  esac
done
echo "Done arg parsing"
require_src()
{
  if [ "${SRC_DIR}xxx" = "xxx" ]
  then
    echo "You must supply a source package with -s"
    exit 1
  fi
}

require_module()
{
  if [ "${MODULE}xxx" = "xxx" ]
  then
    echo "You must supply a module to lint with -m"
    exit 1
  fi
}

$VIRTUALENV_DIR/bin/python setup.py install

[ "${TEST_OUTPUT_DIR}xxx" = "xxx" ] && TEST_OUTPUT_DIR=test_results

mkdir -p $TEST_OUTPUT_DIR

if [ "${PYLINT}xxx" != "xxx" ]
then
  require_module
  $VIRTUALENV_DIR/bin/pylint -f parseable $MODULE | tee $TEST_OUTPUT_DIR/pylint.txt 
fi

if [ "${PEP8}xxx" != "xxx" ] 
then
  require_src
  $VIRTUALENV_DIR/bin/pep8 --format=pylint $SRC_DIR | tee $TEST_OUTPUT_DIR/pep8.txt
fi

if [ "${PYFLAKES}xxx" != "xxx" ]
then
  require_src
  $VIRTUALENV_DIR/bin/pyflakes $SRC_DIR | awk -F\: '{printf "%s:%s: [E]%s\n", $1, $2, $3}' | tee $TEST_OUTPUT_DIR/pyflakes.txt 
fi
