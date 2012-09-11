#!/usr/bin/env bash

# Initialize variables
test -z $DEV_TOOLS_HOME || DEV_TOOLS_HOME=${HOME}/.snakegit
test -z $PIP_DOWNLOAD_CACHE || PIP_DOWNLOAD_CACHE=`pwd`/vendor/cache
test -z $VIRTUALENV_DIR || VIRTUALENV_DIR=`pwd`/vendor/python
test -z $TEST_OUTPUT_DIR || TEST_OUTPUT_DIR=`pwd`/test_reports

# run build
$DEV_TOOLS_HOME/bin/build.sh

function usage {
	echo "test [options]"
	echo ""
	echo "-h|--help                    Show this message"
	echo "-x|--xunit                   Generate an XUnit compatible report"
	echo "-c|--coverage                Generate a test coverage report"
	echo "-p|--cover-package=<pkg>     Which package should have coverage measured"
	echo "-w|--test-dir=<dir>          Which directory holds the tests"
}

ARGS=`getopt -o hxcpw: -l help,xunit,coverage,cover-package:,test-dir: -- "$@"`

test $? -eq 0 || exit 1

eval set -- "$ARGS"

while [ $# -gt 0 ];
do
	case "$1" in
		
		-h|--help)
			usage
			exit 0
			;;

		-x|--xunit)
			JUNIT_OPTS="--with-xunit --xunit-file=$TEST_OUTPUT_DIR/nosetests.xml"
			shift;;
			
		-c|--coverage)
			COVERAGE_OPTS="--with-coverage --cover-xml \
				--cover-xml-file=$TEST_OUTPUT_DIR/coverage.xml"
			shift;;

		-p|--cover-package)
			if [ -n "$2" ]
			then
				COVER_PACKAGE_OPTS="--cover-package=$2"
			fi
			shift 2;;

		-w|test-dir)
			if [ -n "$2" ]
			then
				TEST_DIR=$2
			fi
		shift 2;;

		--)
			shift
			break;;

		-*)
			usage 1>&2
			exit
			;;
		*)
			usage 1>&2
			exit
			;;
	esac
	shift
done

# Build before running tests
/usr/bin/env bash $DEV_TOOLS_HOME/bin/build.sh

mkdir -p $TEST_OUTPUT_DIR

# Install any test requirements
if [ -f test-requirements.txt ]
then
	echo "Installing test dependencies"
	PIP_DOWNLOAD_CACHE=$PIP_DOWNLOAD_CACHE $VIRTUALENV_DIR/bin/pip install \
		-r test-requirements.txt > /dev/null
fi

# Install nose an coverage
echo "Setting up test environment"
$VIRTUALENV_DIR/bin/pip freeze | grep -q nose || $VIRTUALENV_DIR/bin/pip install \
	$DEV_TOOLS_HOME/var/submodules/nose > /dev/null
$VIRTUALENV_DIR/bin/pip install coverage > /dev/null

# Execute nose tests
NOSE_OPTS="$COVERAGE_OPTS $COVER_PACKAGE_OPTS $JUNIT_OPTS $TEST_DIR" 
$VIRTUALENV_DIR/bin/nosetests $NOSE_OPTS 
