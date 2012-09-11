#!/usr/bin/env sh

# Initialize variables
test "xxx${DEV_TOOLS_HOME}" = "xxx"     && DEV_TOOLS_HOME=${HOME}/.snakegit
test "xxx${PIP_DOWNLOAD_CACHE}" = "xxx" && PIP_DOWNLOAD_CACHE=`pwd`/vendor/cache
test "xxx${VIRTUALENV_DIR}" = "xxx"     && VIRTUALENV_DIR=`pwd`/vendor/python
test "xxx${TEST_OUTPUT_DIR}" = "xxx"    && TEST_OUTPUT_DIR=`pwd`/test_reports

# run build
$DEV_TOOLS_HOME/bin/build.sh

usage()
{
	echo "test [options]"
	echo ""
	echo "-h                    Show this message"
	echo "-x                    Generate an XUnit compatible report"
	echo "-c                    Generate a test coverage report"
	echo "-p=<pkg>              Which package should have coverage measured"
	echo "-w=<dir>              Which directory holds the tests"
}

while getopts hxcpw: o
do 
	case "$o" in
		
		h)
			usage
			exit 0
			;;

		x)
			JUNIT_OPTS="--with-xunit --xunit-file=$TEST_OUTPUT_DIR/nosetests.xml"
			;;
			
		c)
			COVERAGE_OPTS="--with-coverage --cover-xml \
				--cover-xml-file=$TEST_OUTPUT_DIR/coverage.xml"
			;;

		p)
			COVER_PACKAGE_OPTS="--cover-package=$OPTARG"
			;;

		w)
			TEST_DIR="$OPTARG"
			;;	

		[?])
			usage 1>&2
			exit
			;;
	esac
done
#shift $OPTIND-1

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
