#!/usr/bin/env sh

[ "${SNAKEGIT_HOME}xxx" = "xxx" ] &&  SNAKEGIT_HOME=${HOME}/.snakegit
[ "${VIRTUALENV_DIR}xxx" = "xxx" ] &&  VIRTUALENV_DIR=`pwd`/vendor/python

package() {
  PACKAGE_NAME=$($VIRTUALENV_DIR/bin/python setup.py --name)
  VERSION=$($VIRTUALENV_DIR/bin/python setup.py --version)
  while getopts s o
  do
    case $o in

      s)
        VERSION="$VERSION-`date +%s`"
        ;;

      [?])
        echo >&2 "Usage: $0 package [-s]"
        exit 1
        ;;
    esac
  done
  echo "Building package"

  ${SNAKEGIT_HOME}/bin/build.sh

  ${VIRTUALENV_DIR}/bin/python setup.py install

  ${SNAKEGIT_HOME}/bin/virtualenv --relocatable ${VIRTUALENV_DIR}

  mkdir -p gearbox

  rsync -ar _gb/gbtemplates/ gearbox/gbtemplates/
  [ -e _gb/gbtest ] && rsync -ar _gb/gbtest/ gearbox/gbtest/

  rsync -ar ${VIRTUALENV_DIR}/ gearbox

  mkdir -p gearbox_dist

  current_dir=`pwd`

  tarfile="`pwd`/gearbox_dist/$VERSION.tar.gz"

  cd gearbox

  tar -czvf $tarfile *

  cd $current_dir
}

upload() {
  while getopts e:s o
  do
    case $o in

      e)
        ENVIRONMENT="$OPTARG"
        ;;

      s)
        SNAPSHOT="true"
        ;;

      [?])
        echo >&2 "Usage: $0 -e environment -s"
    esac
  done

  [ "xxx${ENVIRONMENT}" = "xxx" ] && echo >&2 "Usage: $0 -e environment" && exit 1

  PACKAGE_NAME=`${VIRTUALENV_DIR}/bin/python setup.py --name`
  VERSION=`${VIRTUALENV_DIR}/bin/python setup.py --version`

  cd gearbox_dist

  if [ "xxx${SNAPSHOT}" != "xxx" ] 
  then
    ls -lrt $VERSION-*.tar.gz > /dev/null 2>&1
    if [ $? -ne 0 ] 
    then 
      echo >&2 "No version built yet" 
      exit 1
    fi
    ARTIFACT=$(ls -lrt $VERSION-*.tar.gz | awk '{ f=$NF }; END{ print f }')
  else
    ARTIFACT="$VERSION.tar.gz"
  fi
  echo -n "Upload $ARTIFACT to $ENVIRONMENT [Y]? "
  read RESPONSE
  if [ "$RESPONSE" = "y" ] || [ "$RESPONSE" = "Y" ] || [ "${RESPONSE}Y" = "Y" ] 
  then
    echo "Uploading gearbox artifact"
    $SNAKEGIT_HOME/bin/python $SNAKEGIT_HOME/bin/gearboxupload.py -b s3_ops -e $ENVIRONMENT -n $PACKAGE_NAME -f $ARTIFACT
  else
    echo >&2 "Ok, not uploading artifact"
    exit 1
  fi
}

case $1 in

  package)
    shift
    package $@
    ;;

  upload)
    shift
    upload $@
    ;;

  *)
    echo >&2 "Usage: $0 package|upload [options]"
esac



