#!/usr/bin/env bash


# Initialize variables
test -v DEV_TOOLS_HOME || DEV_TOOLS_HOME=${HOME}/.snakegit
test -v PIP_DOWNLOAD_CACHE || PIP_DOWNLOAD_CACHE=`pwd`/vendor/cache
test -v VIRTUALENV_DIR || VIRTUALENV_DIR=`pwd`/vendor/python
test -v TEST_OUTPUT_DIR || TEST_OUTPUT_DIR=`pwd`/test_reports

# run build
$DEV_TOOLS_HOME/bin/build.sh

ARGS=`getopt -o "xcpw:" -l "xunit,coverage,cover-package:,test-dir:" -- "$@"`

test $? -eq 0 || exit 1

eval set -- "$ARGS"

while true;
do
	case "$1" in
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
	esac
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
